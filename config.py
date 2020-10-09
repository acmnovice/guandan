cardRanks=['2','3','4','5','6','7','8','9','T','J','Q','K','A','B','R']
cardColors=['S','H','C','D']
cardTypes=['StraightFlush', 'Bomb', 'ThreePair', 'TripsPair','ThreeWithTwo', 'Straight', 'Trips', 'Pair', 'Single']

class CompareRank():
    def Larger(self, type, rank, card, formerAction): #('Staight','5','9',['S4','S5','H6','H7,'D8']) -> yes
        r1 = cardRanks.index(rank)
        r2 = cardRanks.index(formerAction['rank'])
        if (type=='Bomb'):
            if (formerAction['type']=='Bomb'):
                if (card>len(formerAction['action'])):
                    return True
                elif (card<len(formerAction['action'])):
                    return False
                else:
                    return cardRanks.index(rank) > cardRanks.index(formerAction['rank'])
            elif (formerAction['type']=='StraightFlush'):
                if card>5:
                    return True
                else:
                    return False
            else:
                return True
        elif (type=='Trips' or type=='Pair' or type=='Single' or type=='ThreeWithTwo'):
            return r1 > r2
        elif (type=='ThreePair' or type=='TripsPair' or type=='Straight'):
            if (r1 == cardRanks.index('A')): r1 = -1
            if (r2 == cardRanks.index('A')): r2 = -1
            return r1 > r2

#print(CompareRank().Larger('Bomb','T',4,{'type':'Bomb','rank':'A','action':['SA', 'HA', 'HA', 'DA']}))


