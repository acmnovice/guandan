import config
import CountValue
class Strategy(object):
    def Clear(self):
        self.roundStage = ''
        self.role = ''
        self.actionValueRevise = {}
        self.handValueRevise = {}
        self.restCardsCount = {}
        self.restHandsCount = []
        self.PlayersTypeMsg = None
        self.curPos = -1
        self.greaterPos = -1
        self.myPos = -1
        self.greaterAction = None
        self.curAction = None
        self.curRank = None
        self.recordPlayerActions = [{},{},{},{}]

    def __init__(self):
        self.Clear()

    def foo(self):
        pass

    def SetBeginning(self, myPos):
        self.Clear()
        self.roundStage = 'beginning'
        self.myPos = myPos
        self.restHandsCount = [27, 27, 27, 27]
        self.recordPlayerActions = [{},{},{},{}]
        for rank in config.cardRanks:
            if rank=='B' or rank=='R':
                self.restCardsCount[rank]=2
            else:
                self.restCardsCount[rank]=4

    def SetRole(self, handValue, handActions, curRank):
        countBombs=0
        countBigs=0
        countSmalls=0
        for action in handActions:
            actionValue = CountValue.CountValue().ActionValue(action, action['type'], action['rank'], curRank)
            if action['type'] == 'Bomb' or action['type']=='StraightFlush':
                countBombs += 1
            elif actionValue < 0:
                countSmalls += 1
            else:
                countBigs += 1
        #print(handValue, handActions, curRank)
        #print('bombs:',countBombs,'bigs',countBigs,'smalls:',countSmalls)
        self.role = ""
        if (countSmalls<=3 and countBombs>=3):
            self.role += "active attack"
        elif (countSmalls<=3 and countBigs>=3):
            self.role += "active defense"
        elif (countSmalls<=3 and countBombs<3):
            self.role += "defense"
        elif (countBigs>3 and countBombs>=3):
            self.role += "pair attack"
        elif (countSmalls>3 and countBigs>=3):
            self.role += "pair defense"
        elif (countSmalls>3):
            self.role = "pair defense"

    def UpdateCurRank(self, curRank):
        self.curRank = curRank

    def UpdatePlay(self, curPos, curAction, greaterPos, greaterAction): #'3', ['Pair','3','['S3','H3']]
        self.restHandsCount[curPos] -= len(curAction[2])
        if (self.restHandsCount[curPos]<=10):
            self.roundStage = 'ending'
        self.curAction = curAction
        self.curPos = curPos
        self.greaterPos = greaterPos
        self.greaterAction = greaterAction

        if (curAction[0]=='PASS'):  #update recordPlayerActions
            type = greaterAction[0]
            rank = 'PASS'
        elif (curAction[0]=='Bomb' and greaterAction[0]!='Bomb'):
            type = greaterAction[0]
            rank = 'Bomb'
        else:
            type = curAction[0]
            rank = curAction[1]

        if type not in self.recordPlayerActions[curPos].keys():
            self.recordPlayerActions[curPos][type] = [rank]
        else:
            self.recordPlayerActions[curPos][type].append(rank)

    def UpdateRVByRoleAtBeginning(self):
        if (self.roundStage != 'beginning'):
            return
        if ('defense' in self.role):
            self.actionValueRevise['Bomb'] = max(-0.5, self.actionValueRevise['Bomb']-0.5)
            self.handValueRevise["Bomb"] = 0
        if ('active' in self.role):
            self.actionValueRevise['Bomb'] = 0
            self.handValueRevise["Bomb"] = max(-0.5, self.handValueRevise['Bomb']-0.5)
        #print('here')

    def UpdateRVATEnding(self):
        if (self.roundStage != 'ending'):
            return
        self.actionValueRevise['Bomb'] = max(0, self.actionValueRevise['Bomb'])
        self.handValueRevise["Bomb"] = 0
        self.actionValueRevise["Straight"] = min(1, self.handValueRevise['Straight'] + 0.5)
        self.handValueRevise["Straight"] = max(-1, self.handValueRevise['Straight']-0.5)
        self.actionValueRevise["TwoTrips"] = min(1, self.handValueRevise['TwoTrips'] + 0.5)
        self.handValueRevise["TwoTrips"] = max(-1, self.handValueRevise['TwoTrips']-0.5)
        self.actionValueRevise["ThreePair"] = min(1, self.handValueRevise['ThreePair'] + 0.5)
        self.handValueRevise["ThreePair"] = max(-1, self.handValueRevise['ThreePair']-0.5)

    def UpdateRVByRestHandsCount(self):
        if (self.roundStage != 'ending'):
            return
        C_part = self.restHandsCount[(self.myPos+2)%4]
        C_oppo = [self.restHandsCount[(self.myPos+1)%4], self.restHandsCount[(self.myPos+3)%4]]
        if (C_part == 1):
            self.actionValueRevise['Single'] += 1
        elif (C_part == 2):
            self.actionValueRevise['Pair'] += 1
        if (C_part == 5):
            self.actionValueRevise['Pair'] -= 1
            self.actionValueRevise['ThreeWithTwo'] += 0.5
        if (1 in C_oppo):
            self.actionValueRevise['Single'] -= 1
        elif (2 in C_oppo):
            self.actionValueRevise['Pair'] -= 1
        if (5 in C_oppo):
            self.actionValueRevise['Pair'] += 1
            self.actionValueRevise['ThreeWithTwo'] -= 1

    def UpdateRVWhenPartnerControls(self):
        if (self.greaterPos == (self.myPos+2)%4):
            self.actionValueRevise['Bomb'] = -1
            self.actionValueRevise["StraightFlush"] = -1
            self.actionValueRevise["Single"] = max(-1, self.handValueRevise['Single']-0.5)
            self.actionValueRevise["Pair"] = max(-1, self.handValueRevise['Pair'] - 0.5)
            self.actionValueRevise["Trips"] = max(-1, self.handValueRevise['Trips'] - 0.5)
            self.actionValueRevise["Straight"] = max(-1, self.handValueRevise['Straight'] - 0.5)
            self.actionValueRevise["ThreeWithTwo"] = max(-1, self.handValueRevise['ThreeWithTwo'] - 0.5)

    def UpdateRVwhenOppoPlaysSmall(self):
        if (self.greaterPos !=(self.myPos+1)%4 and self.greaterPos !=(self.myPos+3)%4):
            self.actionValueRevise["PASS"] = 0
            return
        elif (self.greaterPos ==(self.myPos+1)%4):
            oppoHandValue = CountValue.CountValue().ActionValue(self.curAction[2], self.curAction[0], self.curAction[1], self.curRank)
            part = (self.myPos + 2) % 4
            if self.curAction[0] in self.recordPlayerActions[part].keys():
                if self.recordPlayerActions[part][self.curAction[0]][-1] in ['PASS','Bomb']:
                    self.actionValueRevise["PASS"] = max(-1, min(0, oppoHandValue))
                    return
        self.actionValueRevise["PASS"] = 0
        return

    def UpdateRVByPlayerActions(self):
        oppo1 = (self.myPos+1)%4
        part = (self.myPos+2)%4
        oppo2 = (self.myPos+3)%4
        for type in config.cardTypes:
            value = 0
            if type in self.recordPlayerActions[oppo1].keys():
                if self.recordPlayerActions[oppo1][type][-1] in ['PASS','Bomb']:
                    value += 0.5
            if type in self.recordPlayerActions[oppo2].keys():
                if self.recordPlayerActions[oppo2][type][-1] in ['PASS','Bomb']:
                    value += 0.5
            '''if type in self.recordPlayerActions[part].keys():
                if self.recordPlayerActions[part][type][-1] in ['PASS','Bomb']:
                    value -= 0.5'''
            self.actionValueRevise[type] = min(1,max(-1, self.handValueRevise[type] + value))

    def UpdateRVwhenRushing(self):
        C_myself = self.restHandsCount[self.myPos]
        if (C_myself > 5):
            return
        if C_myself == 2:
            self.actionValueRevise['Single'] = max(0.5, self.actionValueRevise['Single'] + 0.5)
            self.actionValueRevise['PASS'] = min(-1, self.actionValueRevise['PASS'] - 0.5)
        if C_myself == 3 or C_myself == 4:
            self.actionValueRevise['Single'] = max(0.5, self.actionValueRevise['Single'] + 0.5)
            self.actionValueRevise['Pair'] = max(0.5, self.actionValueRevise['Pair'] + 0.5)
            self.actionValueRevise['PASS'] = min(-1, self.actionValueRevise['PASS'] - 0.5)

    def makeReviseValues(self):
        for type in config.cardTypes:
            self.actionValueRevise[type] = 0
            self.handValueRevise[type] = 0
        self.UpdateRVByRoleAtBeginning()
        self.UpdateRVATEnding()
        self.UpdateRVByRestHandsCount()
        self.UpdateRVWhenPartnerControls()
        self.UpdateRVwhenOppoPlaysSmall()
        #self.UpdateRVByPlayerActions()
        self.UpdateRVwhenRushing()

Strategy = Strategy()