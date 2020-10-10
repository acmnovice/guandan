from CreateActionList import CreateActionList
from CountValue import CountValue
from config import CompareRank
import config
import json

class PlayCard():

    def FreePlay(self, handCards, curRank):
        print("Free play handCards:", handCards)
        handValue, handActions = CountValue().HandCardsValue(handCards, 1, curRank)
        bestPlay = {}
        minValue = 100
        for action in handActions:
            actionValue = CountValue().ActionValue(action, action['type'], action['rank'], curRank)
            if actionValue < minValue:
                minValue = actionValue
                bestPlay = action

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
        #print(actionList)
        bestPlay = []
        maxValue, restActions = CountValue().HandCardsValue(handCards, 1, curRank)

        for i in range(0, len(config.cardTypes)):
            type = config.cardTypes[i]
            #print(type, formerAction["type"])
            if (type == 'StraightFlush'): continue
            if (type != 'Bomb' and type != formerAction["type"]): continue
            for rank in actionList[type]:
                for card in actionList[type][rank]:
                    #print("Restricted play trying rank, card:", rank, card)
                    if (CompareRank().Larger(type, rank, card, formerAction, curRank)):
                        action = CreateActionList().GetAction(type, rank, card, handCards)
                        restCards = CreateActionList().GetRestCards(action, handCards)
                        restValue, restActions = CountValue().HandCardsValue(restCards, 1, curRank)
                        thisHandValue = CountValue().ActionValue(action, type, rank, curRank)
                        if (thisHandValue < 0): thisHandValue = 0
                        if (thisHandValue + restValue > maxValue or (thisHandValue + restValue == maxValue and (thisHandValue > 0 or bestPlay==[]))):
                            maxValue = restValue
                            bestPlay = {"action": action, "type": type, "rank": rank}

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

