import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from copy import deepcopy
import random
import ray

#SOURCES:
#Source1: https://github.com/matteocasolari/reinforcement-learning-an-introduction-solutions/blob/master/exercises/Exercise4.7.py
#Got the idea for using 4 nested for loops for the rental and returs rather than two sets of 2 for loops one for each location.
#Used their V printing technique 
#Used uncover the slowdown in my original implementation which used scipy for poisson cdf and pmf rather than implementing it myself
#Source2: https://stackoverflow.com/questions/22083601/how-to-speed-up-poisson-pmf-function
#Used their implementation of pmd and cdf for poisson variables 
#Source3: https://towardsdatascience.com/modern-parallel-and-distributed-python-a-quick-tutorial-on-ray-99f8d70369b8
#Got the idea of using Ray for multiprocessing the Policy Improvement from here

maxCars = 10
gamma = .9
returnLam1 = 3
rentalLam1 = 3
returnLam2 = 2
rentalLam2 = 4
rentalReward = 10
carTransferPenalty = -2
theta = .01

#Source 2
def poisson_pmf(x, mu):
    return (mu**x / math.factorial(x)) * math.exp(-mu)

#Source 2
def poisson_cdf(k, mu):
    return sum(poisson_pmf(x, mu) for x in range(k+1))
    # p_total = 0.0
    # for x in range(k+1):
    #     p_total += poisson_pmf(x, mu)
    # return p_total

#Source1
def qsa(state: tuple, action: int):
    l1Count = state[0]-action
    l2Count = state[1]+action
    actionCost = abs(action) * carTransferPenalty

    value = 0
    for i in range(l1Count+1): #for number of cars rented from l1
        l1Reward = i * rentalReward
        iProb = (1-poisson_cdf(l1Count-1,rentalLam1)) if (i == l1Count) else poisson_pmf(i,rentalLam1)
        for j in range(maxCars - l1Count + i + 1): #for number of cars returned at l1 given i cars rented
            l1Prob = iProb * ((1-poisson_cdf((maxCars-l1Count+i-1),returnLam1)) if (j==(maxCars-l1Count+i)) else (poisson_pmf(j,returnLam1)))
            for k in range(l2Count+1): #for number of cars rent from l2
                l2Reward = k * rentalReward
                kProb = (1-poisson_cdf(l2Count-1,rentalLam2)) if (k == l2Count) else poisson_pmf(k,rentalLam2)
                for l in range(maxCars - l2Count + k + 1): #for number of cars returned at l2 given k cars rented
                    l2Prob = kProb * ((1-poisson_cdf((maxCars-l2Count+k-1),returnLam2)) if (l==(maxCars-l2Count+k)) else (poisson_pmf(l,returnLam2)))
                    value += l1Prob * l2Prob * (l1Reward + l2Reward + actionCost + gamma * V[(l1Count - i + j)][(l2Count - k + l)])
    return value

#list all 
availableActions = {}
for i in range(maxCars + 1):
    for j in range(maxCars + 1):
        availableActions[(i,j)] = [0]
        for k in range(1,6):
            if j-k >= 0 and i+k <= (maxCars):
                availableActions[(i,j)].append(-k)
            if i-k >= 0 and j+k <= (maxCars):
                availableActions[(i,j)].append(k)

Pi  = np.zeros((maxCars + 1, maxCars + 1), dtype=int)
Pis = [deepcopy(Pi)]
V = np.zeros((maxCars + 1, maxCars + 1))
Vs = []

@ray.remote
def MultiHelper(l1Cars,l2Cars):
    bestAction = 0
    maxValue = 0
    for action in availableActions[(l1Cars, l2Cars)]:
        value = qsa((l1Cars,l2Cars), action)
        if value > maxValue:
            maxValue = value
            bestAction = action
    return bestAction

if __name__ == '__main__':
    while(True):
        ray.init()
        print("policy evaluation")
        #Policy Evaluation
        while (True):
            delta = 0
            for l1Cars in range(maxCars + 1):
                for l2Cars in range(maxCars + 1):
                    currentBestAction = Pi[l1Cars][l2Cars]
                    newVi = qsa((l1Cars,l2Cars), currentBestAction)
                    oldVi = V[l1Cars][l2Cars]
                    V[l1Cars][l2Cars] = newVi
                    delta = max(delta, abs(oldVi - newVi))

            print("eval iteration")
            if (delta < theta):
                break
        Vs.append(deepcopy(V))

        for row in V:
            for col in row:
                print("%.2f" % col, end="|")
            print()
            print("----------------------------------------------------------------")
        print()

        #Source3
        print("policy Improvement")
        newPiIds = []
        policyStable = True
        for l1Cars in range(maxCars + 1):
            for l2Cars in range(maxCars + 1):
                newPiIds.append(MultiHelper.remote(l1Cars,l2Cars))
        newPi = np.array(ray.get(newPiIds)).reshape([(maxCars+1),(maxCars+1)])
        nuwPiIds = None
        print(newPi)
        if np.array_equal(Pi, newPi) == False:
            policyStable = False
        Pi = newPi
        Pis.append(deepcopy(Pi))

        ray.shutdown()

        if policyStable:
            break

    fig1, axes1 = plt.subplots(len(Pis)//2+1,2)
    fig1.suptitle("Policy Improvement")
    for i in range(len(Pis)):
        plotX = i // 2
        plotY = i % 2 
        im = axes1[plotX,plotY].imshow(Pis[i], origin='lower', interpolation='nearest')
        fig1.colorbar(im, ax=axes1[plotX,plotY])        
        axes1[plotX,plotY].set_xlabel('Location1 Cars')
        axes1[plotX,plotY].set_ylabel('Location2 Cars')
        axes1[plotX,plotY].set_title('pi(' + str(i) + ')')
        

    #Source #1
    fig2, axes2 = plt.subplots(len(Vs)//2+1,2,subplot_kw={'projection':'3d'})
    fig2.suptitle("Policy Evaluation")
    for i in range(len(Vs)):
        X = np.arange(0,maxCars+1)
        Y = np.arange(0,maxCars+1)
        X,Y = np.meshgrid(X,Y)
        plotX = i //2
        plotY = i % 2
        if (i > 0):
            axes2[plotX,plotY].plot_surface(X,Y,np.subtract(Vs[i],Vs[i-1]),cmap='Reds')
            axes2[plotX,plotY].set_xlabel('Location1 Cars')
            axes2[plotX,plotY].set_ylabel('Location2 Cars')
            axes2[plotX,plotY].set_zlabel('State Value Change')
            axes2[plotX,plotY].set_title('V(pi(' +str(i) +')) - V(pi(' +str((i-1)) +'))')
        if (i == 0):
            axes2[plotX,plotY].plot_surface(X,Y,Vs[i])
            axes2[plotX,plotY].set_xlabel('Location1 Cars')
            axes2[plotX,plotY].set_ylabel('Location2 Cars') #, labelpad=10)
            axes2[plotX,plotY].set_zlabel('Value')
            axes2[plotX,plotY].set_title('V(pi(' +str(i) +'))')
        if (i == len(Vs)-1):
            #final is the next panel after the change graph for the final policy
            final = i+1
            plotX = final //2
            plotY = final % 2
            axes2[plotX,plotY].plot_surface(X,Y,Vs[i])
            axes2[plotX,plotY].set_xlabel('Location1 Cars')
            axes2[plotX,plotY].set_ylabel('Location2 Cars') #, labelpad=10)
            axes2[plotX,plotY].set_zlabel('Value')
            axes2[plotX,plotY].set_title('V(pi(' +str(final) +'))')


    
    plt.show()
