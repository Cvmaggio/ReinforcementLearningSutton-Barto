import numpy as np
import random as r
#Player will always hit small numbers until they get 12 or more without fear of busting.
#So we only need to consider player states 12 => 21 which is 10 states
#The dealer plays after the player does so we need only consider their faceup card when deciding on what the player does
#The dealers faceup card could be anything but in this case 10 J Q K are all the same to us because we are playing with a deck with instant replacement of cards
#This gives the dealer 1 => 10 and the ace

usableAceBehaviourPolicy = np.zeros((10,10))
noUsableAceBehaviourPolicy = np.zeros((10,10))
usableAceTargetPolicy = np.zeros((10,10))
noUsableAceTargetPolicy = np.zeros((10,10))

deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]


#shift card value to arrray index
def indexPolicy(playerValue,dealerValue):
    return ((playerValue-12),(dealerValue-2))


def playHand(playerPolicy):
    playerValue = 0
    dealerValue = 0
    playerUsableAces = 0
    dealerUsableAces = 0
    
    #Give players their initial cards
    playerFirstCard = r.choice(deck)
    playerSecondCard = r.choice(deck)
    dealerCard = r.choice(deck)
    if playerFirstCard == 11 or playerSecondCard == 11:
        playerUsableAces += 1
        if playerSecondCard == 11 and playerFirstCard == 11:
            playerValue = 12
        else:
            playerValue = playerFirstCard + playerSecondCard
    else:
        playerValue = playerFirstCard + playerSecondCard
    if dealerCard == 11:
        dealerUsableAces += 1
    dealerValue = dealerCard

    #Players turn
    episodeDetails = []
    transitionTrajectory = []

    while(True):
        playerAction = playerPolicy(indexPolicy(playerValue,dealerValue))
        transitionTrajectory.append([playerValue,dealerValue,playerAction])
        if playerAction == 1: #Player hits
            playerCard = r.choice(deck)
            if playerCard == 11:
                playerUsableAces += 1
            playerValue += playerCard
            while playerValue > 21 and playerUsableAces > 0:
                playerValue -= 10
                playerUsableAces -= 1
            if playerValue > 21:
                print("player bust")
            
            
        else: #Player stays
            print("player stays")
            
