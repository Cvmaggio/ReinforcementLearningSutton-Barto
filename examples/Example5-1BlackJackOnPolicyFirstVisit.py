import numpy as np
import random as r
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
EPISODES = 500000
GAMMA = 1
PLAYEROFFSET = 12
DEALEROFFSET = 2
#The deck of cards being drawn from is each card taken immediately replaced
#face cards act the same as 10 so they are 10 here
deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]

#Hard coded policy from problem statement as to what each player should do at each hand value
#               A 2 3 4 5 6 7 8 9 101112131415161718192021
dealerPolicy = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
playerPolicy = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0]



def indexState(playerValue,dealerValue):
    return ((playerValue-12),(dealerValue-2))

def playHand():
    #Initially two cards are dealt to the player and dealer,
    #One dealer card is visible to players and both player cards are visible
    #The player and dealers hands can be defined by the total value of the cards summed
    #   and the number of aces they have (this allows them to deduct 10 points of value if
    #   they go over 21)
    firstCard = r.choice(deck)
    secondCard = r.choice(deck)
    playerUsableAces = 0
    playerValue = firstCard + secondCard
    #already at 22 so need to use one ace immediately 
    if firstCard == 11 and secondCard == 11:
        playerUsableAces += 1
        playerValue = 12
    elif firstCard == 11 or secondCard == 11:
        playerUsableAces += 1
    
    #Give the dealer one card for now. We will reveal there next card later
    firstCard = r.choice(deck)
    dealerUsableAces = 0
    dealerValue = firstCard
    if firstCard == 11:
        dealerUsableAces += 1

    #The player can hit until their value is at least 12 with no fear of busting
    while playerValue < 12:
        nextCard = r.choice(deck)
        playerValue += nextCard
        if nextCard == 11:
            playerUsableAces += 1
        if playerValue > 21: #This should only happen if the player has at least 1 ace
            playerUsableAces -= 1
            playerValue -= 10

    #Keep track of the path the player takes from here on in
    transitionTrajectory = []
    
    #The players turn where policy matters (12 and up)
    while(True):
        playerAction = playerPolicy[playerValue - 1]
        transitionTrajectory.append([playerValue,dealerValue,playerAction,(1 if (playerUsableAces>0) else 0)])
        if playerAction == 1: #Player hits
            nextCard = r.choice(deck)
            if nextCard == 11: #all aces from here have to be used as 1
                playerValue += 1
            else:
                playerValue += nextCard
            if playerValue > 21:
                #print("player bust with " + str(playerValue))
                return [-1,transitionTrajectory]
        else: #Player Stays 
            #print("player statys with " + str(playerValue))
            break
    
    #Dealers turn
    while(True):
        dealerAction = dealerPolicy[dealerValue - 1]
        if dealerAction == 1: #Dealer hits
            nextCard = r.choice(deck)
            if nextCard == 11:
                dealerUsableAces += 1
            dealerValue += nextCard
            while dealerValue > 21 and dealerUsableAces > 0:
                dealerValue -= 10 
                dealerUsableAces -= 1
            if dealerValue > 21:
                #print("dealer bust with " + str(playerValue))
                return [1,transitionTrajectory]
        else: #Dealer stayts
            #print("dealer stays with " + str(dealerValue))
            break
    
    #Both players have chosen to stay now we see who has a better score
    if playerValue > dealerValue:
        return [1, transitionTrajectory]
    elif playerValue == dealerValue:
        return [0, transitionTrajectory]
    else:
        return [-1, transitionTrajectory]

#state space is a 10 by ten grid because we have 10 possibly dealer showing cards
#   and 10 values that matter for the player 12 through 21
#These two are dintinguished by whether the player hit 12 having a usable ace up their sleeve
V = np.random.rand(2,10,10)
Returns = []
for i in range(2):
    iRow = []
    for j in range(10):
        jRow = []
        for k in range(10):
            jRow.append([])
        iRow.append(jRow)
    Returns.append(iRow)

for _ in range(EPISODES):
    playedHand = playHand()
    reward = playedHand[0]
    trajectory = playedHand[1]
    G = 0 + reward#start G with final reward

    #NOTE: This is technically going in the wrong direction, but gamma is 1 so it wont change the outcome
    for step in trajectory:
        G = GAMMA * G + 0
        #Even though this is first visit, we wont see states more than once per episode
        playerValue, dealerValue, action, usableAces = step[0], step[1], step[2], step[3]
        Returns[usableAces][playerValue - PLAYEROFFSET][dealerValue - DEALEROFFSET] += [G]
        curr = Returns[usableAces][playerValue - PLAYEROFFSET][dealerValue - DEALEROFFSET]
        #print(curr)
        V[usableAces][playerValue - PLAYEROFFSET][dealerValue - DEALEROFFSET] = sum(curr)/len(curr)

fig, axes = plt.subplots(2,subplot_kw={'projection':'3d'})
fig.suptitle("Blackjack On Policy State Values 500,000 Episodes")
for i in range(2):
    X = np.arange(1,11)
    Y = np.arange(1,11)
    X, Y = np.meshgrid(X,Y)
    axes[i].plot_surface(X,Y,V[i],cmap=cm.coolwarm)
    axes[i].set_xlabel('Player Card Value')
    axes[i].set_ylabel('Dealer Card Value')
axes[0].set_title('Usable Ace')
axes[1].set_title('No Usable Ace')

plt.show()