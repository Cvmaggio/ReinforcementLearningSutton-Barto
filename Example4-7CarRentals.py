import numpy as np
import matplotlib.pyplot as plt
# import multiprocessing
from multiprocessing import Pool
from scipy.stats.distributions import poisson 
# poisson = scipy.stats.distributions.poisson

maxCars = 10
gamma = .9
returnLam1 = 3
rentalLam1 = 3
returnLam2 = 2
rentalLam2 = 4
rentalReward = 10
carTransferPenalty = -2
theta = .01

def qsa(state: tuple, action: int):
    print("QSA: " + str(state) + str(action))
    l1Count = state[0]-action
    l2Count = state[1]+action
    actionCost = abs(action) * carTransferPenalty

    value = 0
    for i in range(l1Count+1): #for number of cars rented from l1
        l1Reward = i * rentalReward
        iProb = (1-poisson.cdf(l1Count-1,rentalLam1)) if (i == l1Count) else poisson.pmf(i,rentalLam1)
        for j in range(maxCars - l1Count + i + 1): #for number of cars returned at l1 given i cars rented
            l1Prob = iProb * ((1-poisson.cdf((maxCars-l1Count+i-1),returnLam1)) if (j==(maxCars-l1Count+i)) else (poisson.pmf(j,returnLam1)))
            for k in range(l2Count+1): #for number of cars rent from l2
                l2Reward = k * rentalReward
                kProb = (1-poisson.cdf(l2Count-1,rentalLam2)) if (k == l2Count) else poisson.pmf(k,rentalLam2)
                for l in range(maxCars - l2Count + k + 1): #for number of cars returned at l2 given k cars rented
                    l2Prob = kProb * ((1-poisson.cdf((maxCars-l2Count+k-1),returnLam2)) if (l==(maxCars-l2Count+k)) else (poisson.pmf(l,returnLam2)))
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
Pis = [Pi]
V = np.zeros((maxCars + 1, maxCars + 1))

def MultiHelper(index):
    l1Cars = index // (maxCars+1)
    l2Cars = index % (maxCars+1)
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
            for row in V:
                for col in row:
                    print("%.2f" % col, end="|")
                print()
                print("----------------------------------------------------------------")
            print()
            if (delta < theta):
                break

        print("policy Improvement")
        #Policy Improvement with multiprocessing
        policyStable = True
        oldPi = Pi
        with Pool(10) as pool:
            Pi = np.array(pool.map(MultiHelper, range((maxCars+1)**2))).reshape([maxCars+1,maxCars+1])
            Pis.append(Pi)
        print(Pi)
        if np.array_equal(Pi, oldPi) == False:
            policyStable = False
        if policyStable:
            break




        # #Policy Improvement
        # policyStable = True
        # for l1Cars in range(maxCars + 1):
        #     for l2Cars in range(maxCars + 1):
        #         previousAction = Pi[l1Cars][l2Cars]
        #         bestAction = 0
        #         maxValue = 0
        #         for action in availableActions[(l1Cars, l2Cars)]:
        #             value = qsa((l1Cars,l2Cars), action)
        #             if value > maxValue:
        #                 maxValue = value
        #                 bestAction = action
        #         Pi[l1Cars][l2Cars] = bestAction
        #         if (previousAction != bestAction):
        #             policyStable = False
        # for row in Pi:
        #     for col in row:
        #         print(col, end="|")
        #     print()
        #     print("----------------------------------------------------------------")
        # print()

        # if (policyStable):
        #     break

    fig, axes = plt.subplots(len(Pis))

    fig.suptitle('policies')
    for i in range(len(Pis)):
        axes[i].imshow(Pis[i],cmap='hot', origin='lower', interpolation='nearest')
    plt.show()

    # plt.imshow(Pi,cmap='hot', origin='lower', interpolation='nearest')
    # plt.show()
