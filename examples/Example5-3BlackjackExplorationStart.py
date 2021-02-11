import numpy as np
import random as r
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm




EPISODES = 1000000
GAMMA = 1
PLAYEROFFSET = 12
DEALEROFFSET = 2
#The deck of cards being drawn from is each card taken immediately replaced
#face cards act the same as 10 so they are 10 here
deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]

def playHand(PiPlayer,PiDealer,initialState):
    isFirstAction = True
    playerValue, dealerValue, playerUsableAces, dealerUsableAces, startAction = \
        initialState[0], initialState[1], initialState[2], initialState[3], initialState[4]

    #Keep track of the path the player takes from here on in
    transitionTrajectory = []
    
    #The players turn where policy matters (12 and up)
    while(True):
        if isFirstAction:
            playerAction = startAction
            isFirstAction = False
        else:
            playerAction = PiPlayer[playerUsableAces][playerValue - PLAYEROFFSET][dealerValue - DEALEROFFSET]
        transitionTrajectory.append([playerValue,dealerValue,playerAction,(1 if (playerUsableAces>0) else 0)])
        if playerAction == 1: #Player hits
            nextCard = r.choice(deck)
            if nextCard == 11: #all aces from here have to be used as 1
                playerValue += 1
            else:
                playerValue += nextCard
            while playerValue > 21 and playerUsableAces > 0:
                playerValue -= 10 
                playerUsableAces -= 1
            if playerValue > 21:
                return [-1,transitionTrajectory]
        else: #Player Stays 
            # print("player statys with " + str(playerValue))
            break
    
    #Dealers turn
    while(True):
        dealerAction = PiDealer[dealerValue - 1]
        if dealerAction == 1: #Dealer hits
            nextCard = r.choice(deck)
            if nextCard == 11:
                dealerUsableAces += 1
            dealerValue += nextCard
            while dealerValue > 21 and dealerUsableAces > 0:
                dealerValue -= 10 
                dealerUsableAces -= 1
            if dealerValue > 21:
                #print("dealer bust with " + str(dealerValue))
                return [1,transitionTrajectory]
        else: #Dealer stayts
            # print("dealer stays with " + str(dealerValue))
            break
    
    #Both players have chosen to stay now we see who has a better score
    if playerValue > dealerValue:
        # print("player wins " + str(playerValue) + " " + str(dealerValue))
        return [1, transitionTrajectory]
    elif playerValue == dealerValue:
        # print("draw")
        return [0, transitionTrajectory]
    else:
        # print("player loses")
        return [-1, transitionTrajectory]

#state space is a 10 by ten grid because we have 10 possibly dealer showing cards
#   and 10 values that matter for the player 12 through 21
#These two are dintinguished by whether the player hit 12 having a usable ace up their sleeve
Q = np.random.rand(2,10,10,2)
ReturnsCount = []
for i in range(2):
    iRow = []
    for j in range(10):
        jRow = []
        for k in range(10):
            kRow = []
            for l in range(2):
                kRow.append(0)
            jRow.append(kRow)
        iRow.append(jRow)
    ReturnsCount.append(iRow)
#           A 2 3 4 5 6 7 8 9 101112131415161718192021
PiDealer = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
PiPlayer = []
for i in range(2):
    iRow = []
    for j in range(10):
        iRow.append(np.random.choice([0, 1], size=(10)))
    PiPlayer.append(iRow)
    
for i in range(EPISODES):
    # print(i)
    #Generate the initial state for this episode
    startPlayerValue = r.randint(12,21)
    startDealerValue = r.randint(2,11)
    startPlayerUsableAces = r.randint(0,1)
    startDealerUsableAces = 1 if startDealerValue == 11 else 0  
    startAction = r.randint(0,1)

    initialState = [startPlayerValue,startDealerValue,startPlayerUsableAces,startDealerUsableAces,startAction]

    playedHand = playHand(PiPlayer,PiDealer,initialState)
    reward = playedHand[0]
    trajectory = playedHand[1]
    G = 0 + reward#start G with final reward

    #NOTE: This is technically going in the wrong direction, but gamma is 1 so it wont change the outcome
    for step in trajectory:
        G = GAMMA * G + 0
        #Even though this is first visit, we wont see states more than once per episode
        playerValue, dealerValue, action, usableAces = step[0], step[1], step[2], step[3]

        ReturnsCount[usableAces][playerValue - PLAYEROFFSET][dealerValue - DEALEROFFSET][action] += 1
        count = ReturnsCount[usableAces][playerValue - PLAYEROFFSET][dealerValue - DEALEROFFSET][action]
        Q[usableAces][playerValue - PLAYEROFFSET][dealerValue - DEALEROFFSET][action] += (1/count) * (G - Q[usableAces][playerValue - PLAYEROFFSET][dealerValue - DEALEROFFSET][action])
        PiPlayer[usableAces][playerValue - PLAYEROFFSET][dealerValue - DEALEROFFSET] = np.argmax(Q[usableAces][playerValue - PLAYEROFFSET][dealerValue - DEALEROFFSET])
    # print(Returns[1][9][9])
    # print(PiPlayer)
    # print(PiPlayer[0][9][8])
    # print()
print(Q)
print(PiPlayer)

fig1, axes1 = plt.subplots(2)
fig1.suptitle("Blackjack Exploration Start Pi")
for i in range(2):
    im = axes1[i].imshow(PiPlayer[i], origin='lower',interpolation='nearest')
    fig1.colorbar(im, ax=axes1[i])
    axes1[i].set_xlabel('Player Value')
    axes1[i].set_ylabel('Dealer Value')
axes1[0].set_title('Usable Ace')
axes1[1].set_title('No Usable Ace')

plt.show()



# fig, axes = plt.subplots(2,subplot_kw={'projection':'3d'})
# fig.suptitle("Blackjack On Policy State Values 500,000 Episodes")
# for i in range(2):
#     X = np.arange(1,11)
#     Y = np.arange(1,11)
#     X, Y = np.meshgrid(X,Y)
#     axes[i].plot_surface(X,Y,V[i],cmap=cm.coolwarm)
#     axes[i].set_xlabel('Player Card Value')
#     axes[i].set_ylabel('Dealer Card Value')
# axes[0].set_title('Usable Ace')
# axes[1].set_title('No Usable Ace')

# plt.show()