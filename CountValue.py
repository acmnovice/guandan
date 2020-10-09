from CreateActionList import CreateActionList
import config

class CountValue():
    def ActionValue(self, action, type, rank):   #动作:['S2','H2'], type:Single, rank:'2'
        value=0
        if len(action) == 0: return 0
        if type == 'Single':
            if (rank == 'JOKER' and type==1):
                value=0.5
            elif (rank == 'JOKER' and type==0):
                value=0
            elif (rank == '2'):
                value=-0.5
            else :
                value=-1
        elif type == 'Pair':
            if (rank == 'JOKER' and type==1):
                value=1
            elif (rank == 'JOKER' and type==0):
                value=0.5
            elif (rank == '2'):
                value=0
            else :
                value=-1
        elif (type == 'Trips' or type == 'ThreeWithTwo'):
            if (rank == '2'):
                value=0.5
            elif (rank == 'A'):
                value=0
            elif (rank == 'K'):
                value=-0.5
            else:
                value=-1
        elif (type == 'TripsPair' or type == 'Straight' or type =='ThreePair'):
            value = -0.5
        elif (type == 'Bomb'):
            value = 1
        elif (type == 'StraightFlush'):
            value = 1

        return value

    def OnlyPairAndSingleHandValue(self, handCards): #['HA', 'CA', 'S2', 'C2']
        retValue=0
        cardList={}
        for card in handCards:
            if card[1] in cardList.keys():
                cardList[card[1]]+=1
            else:
                cardList[card[1]]=1
        #print(cardList)
        for rank in cardList.keys():
            retValue += self.ActionValue(['S'+ rank,'S'+ rank], 'Pair', rank) * (cardList[rank]//2) \
                      + self.ActionValue(['S'+ rank], 'Single', rank) * (cardList[rank]%2)
        return retValue

    def HandCardsValue(self, handCards, nowType):
        if len(handCards)==0: return 0
        if nowType >= config.cardTypes.index('Pair'):
            return self.OnlyPairAndSingleHandValue(handCards)
        actionList = CreateActionList().CreateList(handCards)
        #print(actionList)
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
                    thisHandValue = self.ActionValue(action, type, rank)
                    restValue = self.HandCardsValue(restCards, i)
                    #print(thisHandValue, restValue)
                    if (thisHandValue + restValue > maxValue):
                        maxValue = thisHandValue + restValue
                        #print(maxValue, action, restCards)
                    #if (len(handCards)>8):
                        #print(thisHandValue + restValue)
        return maxValue


#value = CountValue().ActionValue([[0, '2'],[0, '2']],'Pair','2')
#print(value)

#cards=[[0,'A'],[0,'A'],[1,'A'],[2,'A'],[0,'2'],[2,'2'],[2,'2'],[0,'3'],[0,'3'],[1,'3'],[0,'4'],[0,'4'],[0,'5'],[0,'5'],[0,'6'],[0,'Q'],[0,'Q'],[0,'K'],[0,'K']]
#cards=[[0,'A'],[0,'A'],[1,'A'],[0,'2'],[2,'2'],[2,'2'],[0,'3'],[0,'3'],[0,'4'],[0,'4']]
#cards=[[0, '2'], [2, '2'], [0, '2'], [1, '2'], [3, '4'], [3, '5'], [1, '5'], [0, '5'], [2, '6'], [3, '6'], [2, '7'], [1, '7'], [0, '7'], [2, '7'], [2, '9'], [0, '10'], [3, '10'], [2, '10'], [3, 'J'], [1, 'Q'], [3, 'K'], [0, 'K'], [2, 'K'], [3, 'A'], [2, 'A'], [3, '3'], [0, 'JOKER']]
#cards = ['H2', 'C2', 'D3', 'S4', 'H4', 'C5', 'C5', 'S6', 'D6', 'H8', 'D8', 'S9', 'H9', 'ST', 'CT', 'SJ', 'CJ', 'DJ', 'HQ', 'DQ', 'SK', 'SA', 'HA', 'H7', 'D7', 'SB', 'HR']
#print(CountValue().HandCardsValue(cards,1))
#print(CountValue().OnlyPairAndSingleHandValue([[1, 'A'], [2, '2']]))