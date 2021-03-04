import numpy as np
import random
SIDELENGTH = 60
EPISODES = 50000
GAMMA = 1
EPSILON = .1

#https://towardsdatascience.com/solving-racetrack-in-reinforcement-learning-using-monte-carlo-control-bdee2aa4f04e
class Generator:
    
    #HELPFUL FUNCTIONS
    def widen_hole_transformation(self,racetrack,start_cell,end_cell):
        
        δ = 1
        while(1):
            if ((start_cell[1] < δ) or (start_cell[0] < δ)):
                racetrack[0:end_cell[0],0:end_cell[1]] = -1
                break

            if ((end_cell[1]+δ > SIDELENGTH) or (end_cell[0]+δ > SIDELENGTH)):
                racetrack[start_cell[0]:SIDELENGTH,start_cell[1]:SIDELENGTH] = -1
                break
                
            δ += 1

        return racetrack
    
    def calculate_valid_fraction(self, racetrack):
        '''
        Returns the fraction of valid cells in the racetrack
        '''
        return (len(racetrack[racetrack==0])/(SIDELENGTH**2))

    def mark_finish_states(self, racetrack):
        '''
        Marks finish states in the racetrack
        Returns racetrack
        '''
        last_col = racetrack[0:SIDELENGTH,SIDELENGTH-1]
        last_col[last_col==0] = 2
        return racetrack
    
    def mark_start_states(self, racetrack):
        '''
        Marks start states in the racetrack
        Returns racetrack
        '''
        last_row = racetrack[SIDELENGTH-1,0:SIDELENGTH]
        last_row[last_row==0] = 1
        return racetrack
    
    
    #CONSTRUCTOR
    def __init__(self):
        pass
    
    
    def generate_racetrack(self):
        '''
        racetrack is a 2d numpy array
        codes for racetrack:
            0,1,2 : valid racetrack cells
            -1: invalid racetrack cell
            1: start line cells
            2: finish line cells
        returns randomly generated racetrack
        '''
        racetrack = np.zeros((SIDELENGTH,SIDELENGTH),dtype='int')
        
        frac = 1
        while frac > 0.5:    
            
            #transformation
            random_cell = np.random.randint((SIDELENGTH,SIDELENGTH))
            random_hole_dims = np.random.randint((25,25))
            start_cell = np.array([max(0,x - y//2) for x,y in zip(random_cell,random_hole_dims)])
            end_cell = np.array([min(SIDELENGTH,x+y) for x,y in zip(start_cell,random_hole_dims)])
        
            #apply_transformation
            racetrack = self.widen_hole_transformation(racetrack, start_cell, end_cell)
            frac = self.calculate_valid_fraction(racetrack)
        
        racetrack = self.mark_start_states(racetrack)
        racetrack = self.mark_finish_states(racetrack)
        
        return racetrack

generator = Generator()
track = generator.generate_racetrack()
print(track)

from matplotlib import pyplot as plt
plt.imshow(track, interpolation='nearest')
plt.show()


###############################################################################################################################

MAXSPEED = 5
MINSPEED = 0
SPEEDRANGE = MAXSPEED - MINSPEED + 1

def availableAccelerations(currVelocity):
    allAccelerations = [(-1,-1), (-1,0), (-1,1),\
                        ( 0,-1), ( 0,0), ( 0,1),\
                        ( 1,-1), ( 1,0), ( 1,1)]
    availableAccelerations = []
    for acceleration in allAccelerations:
        candidateVelocity = (currVelocity[0]+acceleration[0],currVelocity[1]+acceleration[1])
        if candidateVelocity[0] >= -5 and candidateVelocity[0] <= 0 and\
                    candidateVelocity[1] <= 5 and candidateVelocity[1] >= 0 and\
                    candidateVelocity != (0,0):
            availableAccelerations.append(acceleration)
    return availableAccelerations

######### Update Pi to reflect current Q
def getQForState(i,j,k,l):
    return np.argmax(Q[i][j][k][l])
getQForStateVectorized = np.vectorize(getQForState)
def updatePi():
    return np.fromfunction(getQForStateVectorized, (SIDELENGTH,SIDELENGTH,SPEEDRANGE,SPEEDRANGE),dtype=int)
############

def getTrackStartLine():
    line = []
    for i,square in enumerate(track[SIDELENGTH-1]):
        if square == 1:
            line.append(i)
    return line

def getTrackFinishLine():
    line = []
    for j,square in enumerate(track[:,SIDELENGTH-1]):
        if square == 2:
            line.append((j,SIDELENGTH-1))
    return line

#                  --------------state---------------|--action--
Q = np.random.rand(SIDELENGTH,SIDELENGTH,SPEEDRANGE,SPEEDRANGE,9)
C = np.zeros((SIDELENGTH,SIDELENGTH,SPEEDRANGE,SPEEDRANGE,9))
Pi = updatePi()
R = -1

#NOTE: im making b stochastic at first for simplicity sake

def resetToStartLine(y,x):
    return SIDELENGTH-1,np.random.choice(getTrackStartLine())

def isInFinishLine(y,x):
    if (y,x) in getTrackFinishLine():
        return True
    return False

def race(usePi,y,x,vY,vX):
    transitionTrajectory = []

    while(True):
        if (usePi):
            action, probability = getTargetPolicyAction(y,x,vY,vX)
        else:
            action, probability = getBehaviourPolicyAction(y,x,vY,vX)
        transitionTrajectory.append([(y,x,vY,vX),action,R,probability])

        y += vY
        x += vX
        vY += action[0]
        vX += action[1]

        if y >= SIDELENGTH or y < 0 or x >= SIDELENGTH or x < 0 or track[y][x] == -1:
            y,x = resetToStartLine(y,x)
            vY = 0
            vX = 0

        if isInFinishLine(y,x):
            break
    return transitionTrajectory



actionKeys = {\
(-1,-1): 0,\
(-1,0): 1,\
(-1,1):2,\
( 0,-1):3,\
( 0,0):4,\
( 0,1):5,\
( 1,-1):6,\
( 1,0):7,\
( 1,1):8\
}

reverseActionKeys = {
0:(-1,-1),\
1:(-1,0),\
2:(-1,1),\
3:( 0,-1),\
4:( 0,0),\
5:( 0,1),\
6:( 1,-1),\
7:( 1,0),\
8:( 1,1)\
}

def getBehaviourPolicyAction(y,x,vY,vX):
    actions = availableAccelerations((vY,vX))
    rand = random.random()
    probabilityOfThisChoice = 0
    QAction = reverseActionKeys[np.argmax(Q[y][x][vY][vX])]
    if QAction in actions:
        if (random.random() > EPSILON):
            probabilityOfThisChoice = 1 - EPSILON + (EPSILON/len(actions))
            action = QAction
        else:
            probabilityOfThisChoice = EPSILON/len(actions)
            action = random.choice(actions)
    else:
        probabilityOfThisChoice = 1/len(actions)
        action = random.choice(actions)
    return action, probabilityOfThisChoice

def getTargetPolicyAction(y,x,vY,vX):
    actions = availableAccelerations((vY,vX))
    probabilityOfThisChoice = 0
    PiAction = reverseActionKeys[Pi[y][x][vY][vX]]
    if PiAction in actions:
        probabilityOfThisChoice = 1
        action = PiAction
    else:
        probabilityOfThisChoice = 1/len(actions)
        action = random.choice(actions)
    return action, probabilityOfThisChoice

    

for i in range(EPISODES):
    if i%1000 == 0 or i == 1:
        print(i)
    trajectory = race(False,SIDELENGTH-1,random.choice(getTrackStartLine()),0,0)
    G = 0
    W = 1
    for step in trajectory[::-1]:
        #step [state, action, reward]
        state = step[0]
        action = step[1]
        reward = step[2]
        probability = step[3]
        G = (GAMMA * G) + reward
        C[state[0]][state[1]][state[2]][state[3]][actionKeys[action]] += W
        currC = C[state[0]][state[1]][state[2]][state[3]][actionKeys[action]]
        Q[state[0]][state[1]][state[2]][state[3]][actionKeys[action]] += (W / currC) * (G - Q[state[0]][state[1]][state[2]][state[3]][actionKeys[action]])
        Pi[state[0]][state[1]][state[2]][state[3]] = np.argmax(Q[state[0]][state[1]][state[2]][state[3]])
        if actionKeys[action] != Pi[state[0]][state[1]][state[2]][state[3]]:
            break
        W /= probability

targetRun = race(True,SIDELENGTH-1,random.choice(getTrackStartLine()),0,0)
print(len(targetRun))




plt.show()

