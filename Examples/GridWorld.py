import operator
import random
class MazeGame():
    pos = 0

    # 0 ,1 ,2 ,3 ,4 ,
    # 5 ,6 ,7 ,8 ,9 ,
    # 10,11,12,13,14,
    # 15,16,17,18,19,
    # 20,21,22,23,24
    graph = {
        #direction, nextpos, reward
        0: {'up':(0,-1),'right':(1,0),'down':(5,0),'left':(0,-1)},
        1: {'up':(21,10),'right':(21,10),'down':(21,10),'left':(21,10)},
        2: {'up':(2,-1),'right':(3,0),'down':(7,0),'left':(1,0)},
        3: {'up':(13,5),'right':(13,5),'down':(13,5),'left':(13,5)},
        4: {'up':(4,-1),'right':(4,-1),'down':(9,0),'left':(3,0)},

        5: {'up':(0,0),'right':(6,0),'down':(10,0),'left':(5,-1)},
        6: {'up':(1,0),'right':(7,0),'down':(11,0),'left':(5,0)},
        7: {'up':(2,0),'right':(8,0),'down':(12,0),'left':(6,0)},
        8: {'up':(3,0),'right':(9,0),'down':(13,0),'left':(7,0)},
        9: {'up':(4,0),'right':(9,-1),'down':(14,0),'left':(8,0)},

        10:{'up':(5,0),'right':(11,0),'down':(15,0),'left':(10,-1)},
        11:{'up':(6,0),'right':(12,0),'down':(16,0),'left':(10,0)},
        12:{'up':(7,0),'right':(13,0),'down':(17,0),'left':(11,0)},
        13:{'up':(8,0),'right':(14,0),'down':(18,0),'left':(12,0)},
        14:{'up':(9,0),'right':(14,-1),'down':(19,0),'left':(13,0)},

        15:{'up':(10,0),'right':(16,0),'down':(20,0),'left':(15,-1)},
        16:{'up':(11,0),'right':(17,0),'down':(21,0),'left':(15,0)},
        17:{'up':(12,0),'right':(18,0),'down':(22,0),'left':(16,0)},
        18:{'up':(12,0),'right':(19,0),'down':(23,0),'left':(17,0)},
        19:{'up':(13,0),'right':(19,-1),'down':(24,0),'left':(18,0)},

        20:{'up':(15,0),'right':(21,0),'down':(20,-1),'left':(20,-1)},
        21:{'up':(16,0),'right':(22,0),'down':(21,-1),'left':(20,0)},
        22:{'up':(17,0),'right':(23,0),'down':(22,-1),'left':(21,0)},
        23:{'up':(18,0),'right':(24,0),'down':(23,-1),'left':(22,0)},
        24:{'up':(19,0),'right':(24,-1),'down':(24,-1),'left':(23,0)},
    }

    def move(self,dir: str):
        details = self.graph[self.pos][dir]
        self.pos = details[0]
        return details[1] #return reward for transition

    def getAvailableTransitions(self,pos: int):
        return self.graph[pos]

def showVMap(V):
    for i in range(5):
        for j in range(5):
            print("{:.2f}".format(V[i*5+j])+",", end ='')
        print()
    print()

if __name__ == '__main__':
    game = MazeGame()
    V = [0] * 25
    gamma = .9
    theta = .0001
    directions = ['up','right','down','left']


    while True:
        delta = 0
        for i in range(25):
            availableTransitions = game.getAvailableTransitions(i).values()

            vi = V[i]
            summation = 0
            for transition in availableTransitions:
                nextState = transition[0]
                reward = transition[1]
                summation += .25 * (reward + gamma * V[nextState])
            V[i] = summation
            delta = max(delta,abs(vi-V[i]))
        showVMap(V)
        if (delta < theta):
            break