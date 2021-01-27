import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy


maxCapital = 128
theta = .00000000000001
gamma = 1
pH = .4

largestAvailableBet = {}
for s in range(0,maxCapital+1):
    largestAvailableBet[s] = min(s,maxCapital-s)

V = np.zeros(maxCapital + 1)
R = np.zeros(maxCapital + 1)
V[maxCapital] = 1 #Reward for reaching terminal state
sweeps = []
sweepsmeta = []

def psrsa(pH,s,a):
    if s == 0:
        return {s:1}
    if s == maxCapital:
        return {s:1}
    return {(s+a):pH,(s-a):(1-pH)}

def bellman(s,retType: bool):
    bestAction = 0
    maxValue = 0
    for a in range(largestAvailableBet[s]+1):
        probs = psrsa(pH,s,a)
        value = sum((probs[k]*(R[k]+gamma*V[k])) for k in probs)
        if value > maxValue+10e-16:
        #if value >= maxValue:
            bestAction = a
            maxValue = value
    if retType:
        return bestAction
    return maxValue

def valueIteration():
    while True:
        delta = 0
        for s in range(1,maxCapital):
            vi = V[s]
            V[s] = bellman(s,False)
            delta = max(delta, abs(vi-V[s]))
        sweeps.append(deepcopy(V))
        if delta < theta:
            break
    actions = [0]
    for s in range(1,maxCapital):
        actions.append(bellman(s,True))
    return actions        

if __name__ == "__main__":
    
    actions = valueIteration()
    print(actions)
    plt.figure()
    for sweep in sweeps:
        plt.plot(sweep)
    plt.figure()
    plt.plot(actions,'o')
    plt.show()


