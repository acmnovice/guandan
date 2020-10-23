from CreateActionList import CreateActionList
from CountValue import CountValue
from config import CompareRank
import config
import json
import time
from strategy import Strategy


class PlayCard():

    def actBack(self, handCards, curRank):
        bestPlay = []
        maxValue = -100
        for rank in config.cardRanks:
            if (rank!=curRank and rank<='9' and rank>='2'):
                for card in handCards:
                    if (card[1]==rank):
                        action = [card]
                        restCards = CreateActionList().GetRestCards(action, handCards)
                        restValue, restActions = CountValue().HandCardsValue(restCards, 0, curRank)
                        if (restValue>maxValue):
                            maxValue = restValue
                            bestPlay = {"action": action, "type": "back", "rank": rank}
                        #print(card, restValue)
                        break
        return bestPlay

    def FreePlay(self, handCards, curRank):
        print("Free play handCards:", handCards)
        handValue, handActions = CountValue().HandCardsValue(handCards, 0, curRank)
        #print(handActions)
        #Strategy.SetBeginning(0)
        Strategy.SetRole(handValue, handActions, curRank)
        Strategy.makeReviseValues()
        #print(Strategy.actionValueRevise)
        #print(Strategy.recordPlayerActions)
        bestPlay = {}
        minValue = 100
        for action in handActions:
            actionValue = CountValue().ActionValue(action, action['type'], action['rank'], curRank) - Strategy.freeActionRV[action['type']] \
                          - Strategy.freeActionRV[(action['type'],action['rank'])]
            #print(action, actionValue)
            if actionValue < minValue:
                minValue = actionValue
                bestPlay = action
        #print(Strategy.freeActionRV[('Pair','Q')])
        '''
        maxValue = -100
        actionList = CreateActionList().CreateList(handCards)
        for i in range(0, len(config.cardTypes)):
            type = config.cardTypes[i]
            if (type == 'StraightFlush'): continue
            for rank in actionList[type]:
                for card in actionList[type][rank]:
                    print("Free play trying type, rank, card:", type, rank, card)
                    action = CreateActionList().GetAction(type, rank, card, handCards)
                    restCards = CreateActionList().GetRestCards(action, handCards)
                    #thisHandValue = CountValue().ActionValue(action, type, rank)
                    restValue, restActions = CountValue().HandCardsValue(restCards, 1, curRank)
                    if (restValue > maxValue):
                        maxValue = restValue
                        bestPlay = {"action": action, "type": type, "rank": rank}
                        #print(bestPlay, maxValue)'''
        #print("bestplay:",bestPlay, "handValue", handValue)
        return bestPlay

    def RestrictedPlay(self, handCards, formerAction, curRank):
        print("Restricted Play handCards:", handCards)
        actionList = CreateActionList().CreateList(handCards)

        bestPlay = []
        maxValue, restActions = CountValue().HandCardsValue(handCards, 0, curRank)
        Strategy.SetRole(maxValue, restActions, curRank)
        Strategy.makeReviseValues()
        maxValue += Strategy.restrictedActionRV["PASS"]

        #print(maxValue)
        toc = time.time()
        #print(toc - tic)

        for i in range(0, len(config.cardTypes)):
            type = config.cardTypes[i]
            #print(type, formerAction["type"])
            #if (type == 'StraightFlush'): continue
            if (type != 'Bomb' and type != 'StraightFlush' and type != formerAction["type"]): continue
            for rank1 in actionList[type]:
                for card in actionList[type][rank1]:
                    color = None
                    rank = rank1  # to distinguish StraightFlush from others
                    if (type == 'StraightFlush'):
                        rank = rank1[1]
                        color = rank1[0]
                    #print("Restricted play trying rank, card:", type, rank, card)
                    if (CompareRank().Larger(type, rank, card, formerAction, curRank)):
                        action = CreateActionList().GetAction(type, rank, card, handCards, color)
                        restCards = CreateActionList().GetRestCards(action, handCards)
                        restValue, restActions = CountValue().HandCardsValue(restCards, 0, curRank)
                        restValue += Strategy.handRV[type]
                        thisHandValue = CountValue().ActionValue(action, type, rank, curRank)
                        thisHandValue += Strategy.restrictedActionRV[type]
                        if (type, rank) in Strategy.restrictedActionRV.keys():
                            thisHandValue += Strategy.restrictedActionRV[(type, rank)]
                        #print(Strategy.actionValueRevise)
                        #print(rank, card, thisHandValue, restValue)
                        if (thisHandValue < 0): thisHandValue = 0
                        if (thisHandValue + restValue > maxValue or (thisHandValue + restValue == maxValue and \
                        (bestPlay==[] or CompareRank().Smaller(type, rank, card, bestPlay, curRank)))):
                            maxValue = thisHandValue + restValue
                            bestPlay = {"action": action, "type": type, "rank": rank}
                            print(maxValue, bestPlay)

        if (bestPlay==[]):
            bestPlay = {'action': 'PASS', 'type': 'PASS', 'rank': 'PASS'}
        #print("bestplay:", bestPlay, "maxvalue", maxValue)
        return bestPlay

    def Play(self, handCards, curRank):
        self.FreePlay(handCards, curRank)


#hand_cards = [[1, '3'], [3, '3'], [2, '5'], [3, '5'], [0, '6'], [2, '6'], [0, '7'], [2, '7'], [2, '7'], [0, '7'], [1, '8'], [2, '8'], [3, '9'], [1, '10'], [2, 'J'], [3, 'J'], [1, 'Q'], [2, 'Q'], [3, 'K'], [0, 'K'], [0, 'K'], [2, 'A'], [0, 'A'], [1, '2'], [0, '2'], [0, 'JOKER'], [0, 'JOKER']]
#cards = ['H2', 'C2', 'D3', 'S4', 'H4', 'C5', 'C5', 'S6', 'D6', 'H8', 'D8', 'S9', 'H9', 'ST', 'CT', 'SJ', 'CJ', 'DJ', 'HQ', 'DQ', 'SK', 'SA', 'HA', 'H7', 'D7', 'SB', 'HR']
#formerAction = {"action": ['H5', 'C5'], "type": 'Pair', 'rank': '5'}
#print(PlayCard().FreePlay(cards,'2'))
#print(PlayCard().RestrictedPlay(hand_cards, formerAction))

'''tic = time.time()

cards =  ['H2', 'D2', 'H3', 'H3', 'C3', 'C3', 'C4', 'C4', 'H5', 'H8', 'ST', 'ST', 'HT', 'DT', 'SJ', 'HJ', 'CJ', 'SA', 'HA', 'DA']
Strategy.SetBeginning(0, cards)
Strategy.curRank = '9'
Strategy.restHandsCount=[27, 27, 10, 27]
Strategy.roundStage = 'ending'

Strategy.UpdatePlay(2, ['TwoTrips', 'Q', ['SQ', 'SQ', 'DQ', 'SK', 'SK', 'DK']], 2, ['TwoTrips', 'Q', ['SQ', 'SQ', 'DQ', 'SK', 'SK', 'DK']])

print(PlayCard().RestrictedPlay(cards,{'action':['SQ', 'SQ', 'DQ', 'SK', 'SK', 'DK'], 'type': 'TwoTrips', 'rank': '9'}, '9'))
#print("RV:", Strategy.restrictedActionRV[('Single','R')])
#Strategy.UpdatePlay(1, None, 1, None)
#print(PlayCard().FreePlay(cards, '9'))

toc = time.time()
print(toc-tic)'''

#cards = ['H2', 'C2', 'D3', 'S4', 'H4', 'C5', 'C5', 'S6', 'D6', 'H8', 'D8', 'S9', 'H9', 'ST', 'CT', 'SJ', 'CJ', 'DJ', 'HQ', 'DQ', 'SK', 'SA', 'HA', 'H7', 'D7', 'SB', 'HR']
#print(PlayCard().actBack(cards, '2'))

#print(not CompareRank().Larger('Pair', 'A', 'A', {'action': ['S6', 'H6', 'C6', 'C6'], 'type': 'Bomb', 'rank': '6'}, '3'))