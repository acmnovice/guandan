from CreateActionList import CreateActionList
import config
from strategy import Strategy

class CountValue():
    def ActionValue(self, action, type, rank, curRank):   #动作:['S2','H2'], type:Single, rank:'2'
        value=0
        if len(action) == 0: return 0
        if type == 'Single':
            if (rank == 'R'):
                value=0.5
            elif (rank == 'B'):
                value=0
            elif (rank == curRank):
                value=-0.5
            else :
                value=-1
        elif type == 'Pair':
            if (rank == 'R'):
                value=1
            elif (rank == 'B'):
                value=0.5
            elif (rank == curRank or rank == 'A'):
                value=0
            elif (rank == 'K'):
                value=-0.5
            else :
                value=-1
        elif (type == 'Trips' or type == 'ThreeWithTwo'):
            if (rank == curRank):
                value=0.5
            elif (rank == 'A' or rank == 'K'):
                value=0
            elif (rank == 'Q' or rank == 'J' or rank == 'T'):
                value=-0.5
            else:
                value=-1
        elif (type == 'TwoTrips' or type =='ThreePair'):
            value = -0.5
        elif (type == 'Straight'):
            value = -0.5
        elif (type == 'Bomb'):
            value = 1
        elif (type == 'StraightFlush'):
            value = 1

        return value

    def OnlyPairAndSingleHandValue(self, handCards, curRank): #['HA', 'CA', 'S2', 'C2']
        retValue=0
        retActions=[]
        handCards.sort(key=lambda card: card[1])
        p=0
        while p<len(handCards):
            if (p<len(handCards)-1 and handCards[p][1]==handCards[p+1][1]):
                action = [handCards[p],handCards[p+1]]
                retValue +=self.ActionValue(action, 'Pair', handCards[p][1], curRank)
                retActions.append({'action': action, 'type': 'Pair', 'rank': handCards[p][1]})
                p+=2
            else:
                action = [handCards[p]]
                retValue +=self.ActionValue([handCards[p]], 'Single', handCards[p][1], curRank)
                retActions.append({'action': action, 'type': 'Single', 'rank': handCards[p][1]})
                p+=1
        return retValue, retActions

    def HandCardsValue(self, handCards, nowType, curRank):
        if len(handCards)==0: return 0,[]
        if nowType >= config.cardTypes.index('Pair'):
            return self.OnlyPairAndSingleHandValue(handCards, curRank)
        actionList = CreateActionList().CreateList(handCards)
        #print(actionList)
        bestActions=[]
        maxValue=-100
        for i in range(nowType, len(config.cardTypes)):
            type = config.cardTypes[i]
            if type == 'StraightFlush': continue
            for rank in actionList[type]:
                for card in actionList[type][rank]:
                    #print(type, rank, card)
                    action = CreateActionList().GetAction(type, rank, card, handCards)
                    restCards = CreateActionList().GetRestCards(action, handCards)
                    #print(restCards)
                    thisHandValue = restValue = 0
                    thisHandValue = self.ActionValue(action, type, rank, curRank)
                    restValue, restActions = self.HandCardsValue(restCards, i, curRank)
                    #print(thisHandValue, restValue)
                    if (thisHandValue + restValue > maxValue):
                        maxValue = thisHandValue + restValue
                        bestActions = [{'action': action, 'type': type, 'rank': rank}] + restActions
                        #print(maxValue, action, restCards)
                        #print(thisHandValue + restValue)
        return maxValue, bestActions


#value = CountValue().ActionValue([[0, '2'],[0, '2']],'Pair','2')
#print(value)

#cards=[[0,'A'],[0,'A'],[1,'A'],[2,'A'],[0,'2'],[2,'2'],[2,'2'],[0,'3'],[0,'3'],[1,'3'],[0,'4'],[0,'4'],[0,'5'],[0,'5'],[0,'6'],[0,'Q'],[0,'Q'],[0,'K'],[0,'K']]
#cards=[[0,'A'],[0,'A'],[1,'A'],[0,'2'],[2,'2'],[2,'2'],[0,'3'],[0,'3'],[0,'4'],[0,'4']]
#cards=[[0, '2'], [2, '2'], [0, '2'], [1, '2'], [3, '4'], [3, '5'], [1, '5'], [0, '5'], [2, '6'], [3, '6'], [2, '7'], [1, '7'], [0, '7'], [2, '7'], [2, '9'], [0, '10'], [3, '10'], [2, '10'], [3, 'J'], [1, 'Q'], [3, 'K'], [0, 'K'], [2, 'K'], [3, 'A'], [2, 'A'], [3, '3'], [0, 'JOKER']]
#cards = ['C3', 'H4', 'D4', 'H5', 'H5', 'C5', 'D5', 'D5', 'S6', 'D6', 'H7', 'H8', 'C9', 'D9', 'ST', 'HT', 'CT', 'CT', 'DT', 'HJ', 'CQ', 'DQ', 'SK', 'HA', 'DA', 'H2', 'D2']
#print(CountValue().HandCardsValue(cards,1,'2'))
#print(CountValue().OnlyPairAndSingleHandValue([[1, 'A'], [2, '2']]))
#c=['H4', 'C3', 'D2', 'S4', 'H2']
#print(CountValue().OnlyPairAndSingleHandValue(c,'2'))
#Strategy.SetBeginning("beginning")
#print(Strategy.roundStage)