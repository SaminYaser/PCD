import math
import time
import traceback
import numpy as np
from message import Message


class Agent:
    # suc_cnt = 0
    # fail_cnt = 0
    # sc = 15
    # fc = 5
    # dsa_prob = 0.7
    # row = 1
    # isMax = False
    # mailManager = None
    # agentNo = 0
    # agentName = None
    # population = 0
    # domain_lb = 0.0
    # domain_ub = 0.0
    # velocity = None
    # position = None
    # inbox = None
    # cons_inbox = None

    # pbest_val = None
    # gbest_val = 0.0
    # pbest_position = None
    # gbest_position = 0.0
    # pbestParticleNo = None
    # gbestParticleNo = 0.0
    # neighbors = None
    # parent = 0
    # child = None

    # currentIter = 0

    # maxIteration = 0
    # edgelist = None
    # indexToEdge = None
    # constraints = None
    # cons_cost = None
    # globalRootCost = None
    # w = 0.0

    # c1 = 0.0
    # c2 = 0.0
    # starttime = 0

    def getMailManager(self):
        return self.mailManager

    def __init__(self, mailManager,  AgentNo,  neighbors,  parent,  child,  population,  domain_lb,  domain_ub,  maxIteration,  ismax,  edgelist,  indexToEdge,  constraints,  w,  c1,  c2):
        self.mailManager = mailManager
        self.agentNo = AgentNo
        self.agentName = f"Agent-{self.agentNo}"
        self.population = population
        self.domain_lb = domain_lb
        self.domain_ub = domain_ub
        self.velocity = [0.0] * (self.population)
        self.position = [0.0] * (self.population)
        self.inbox = dict()
        self.cons_inbox = dict()
        self.pbest_position = [0.0] * (self.population)
        self.cons_cost = [0.0] * (self.population)
        self.pbestParticleNo = [-1] * (self.population + 1)

        self.gbestParticleNo = -1
        self.neighbors = neighbors
        self.parent = parent
        self.child = child
        self.maxIteration = maxIteration
        self.edgelist = edgelist
        self.indexToEdge = indexToEdge
        self.constraints = constraints
        self.globalRootCost = [0.0] * (self.population)
        self.isMax = ismax
        self._rng = np.random.default_rng()
        if (ismax):
            self.pbest_val = [4.9E-324] * (self.population)
            self.gbest_val = 4.9E-324
        else:
            self.pbest_val = [1.7976931348623157E308] * (self.population)
            self.gbest_val = 1.7976931348623157E308
        self.w = w
        self.c1 = c1
        self.c2 = c2
        # self.starttime = System.currentTimeMillis()
        self.starttime = int(time.time() * 1000)
        self.currentIter = 0
        self.gbest_position = 0.0
        self.sc = 15
        self.fc = 5
        self.suc_cnt = 0
        self.fail_cnt = 0
        self.row = 1
        self.dsa_prob = 0.7

    def cal_row(self):
        if (self.fail_cnt > self.fc):
            self.row = 0.5 * self.row
        elif (self.suc_cnt > self.sc):
            self.row = min(2 * self.row, 100)
        return self.row

    def initValues(self):
        i = 0
        while (i < self.population):
            randomValue = ((self._rng.random() * (self.domain_ub - self.domain_lb)) + self.domain_lb)
            # randomValue = ((0.5 * (self.domain_ub - self.domain_lb)) + self.domain_lb)
            assert (randomValue <= self.domain_ub and randomValue >= self.domain_lb)
            # double randomValue = this.domain_lb + (this.domain_ub - this.domain_lb) *
            # r.nextDouble();
            # double randomValueVx = ((Math.random() * (1.0 - 0.0)) + 0.0);
            self.position[i] = randomValue
            self.velocity[i] = 0
            i += 1

    def initValues_example_trace(self):
        a1 = [-1.0, -2.0, 0.0, 1.1]
        a2 = [1.2, 2.0, 1.0, -1.0]
        a3 = [-2.0, -1.0, 2.0, 1.5]
        a4 = [2.0, 1.0, -2.0, 0.5]
        i = 0
        while (i < self.population):
            if (self.agentNo == 0):
                self.position[i] = a1[i]
            elif (self.agentNo == 1):
                self.position[i] = a2[i]
            elif (self.agentNo == 2):
                self.position[i] = a3[i]
            elif (self.agentNo == 3):
                self.position[i] = a4[i]
            self.velocity[i] = 0
            i += 1

    def updateValues(self):
        ub = 1.0
        lb = 0.0
        r1 = (self._rng.random() * (ub - lb)) + lb
        r2 = (self._rng.random() * (ub - lb)) + lb
        # r1 = (0.6 * (ub - lb)) + lb
        # r2 = (0.7 * (ub - lb)) + lb
        i = 0
        while (i < self.population):
            if (i == self.gbestParticleNo):
                self.velocity[i] = -self.position[i] + self.gbest_position + \
                    (self.w * self.velocity[i]) + \
                    self.cal_row() * (1 - (2 * r2))
                self.position[i] = self.position[i] + self.velocity[i]
            else:
                self.velocity[i] = self.w * self.velocity[i] + self.c1 * r1 * (
                    self.pbest_position[i] - self.position[i]) + self.c2 * r2 * (self.gbest_position - self.position[i])
                self.position[i] = self.position[i] + self.velocity[i]
            if (self.position[i] < self.domain_lb):
                self.position[i] = self.domain_lb
            if (self.position[i] > self.domain_ub):
                self.position[i] = self.domain_ub
            i += 1

    def updateValues_example_trace(self):
        r1 = 0.7
        r2 = 0.4
        w = 0.72
        c1 = 1.49
        c2 = 1.49
        i = 0
        while (i < self.population):
            if (i == self.gbestParticleNo):
                self.velocity[i] = -self.position[i] + self.gbest_position + \
                    (w * self.velocity[i]) + self.cal_row() * (1 - (2 * r2))
                self.position[i] = self.position[i] + self.velocity[i]
            else:
                self.velocity[i] = w * self.velocity[i] + c1 * r1 * (
                    self.pbest_position[i] - self.position[i]) + c2 * r2 * (self.gbest_position - self.position[i])
                self.position[i] = self.position[i] + self.velocity[i]
            if (self.position[i] < self.domain_lb):
                self.position[i] = self.domain_lb
            if (self.position[i] > self.domain_ub):
                self.position[i] = self.domain_ub
            i += 1
        print("velocity " + str(self.agentNo) + " = ", end="")
        i = 0
        while (i < self.population):
            print(str(self.velocity[i]) + ",", end="")
            i += 1
        print("")
        print("position " + str(self.agentNo) + " = ", end="")
        i = 0
        while (i < self.population):
            print(str(self.position[i]) + ",", end="")
            i += 1
        print("")

    def sendValueMessage(self):
        try:
            for neigh in self.neighbors:
                valueMsg = Message(self.agentNo, neigh, 202, self.position)
                self.mailManager[neigh].putMessage(valueMsg)
        except Exception as e:
            traceback.print_exc()

    def receiveValueMessage(self):
        try:
            cnt = 0
            while (cnt < len(self.neighbors)):
                rcvdValueMsg = self.mailManager[self.agentNo].getMessage()
                self.inbox[rcvdValueMsg.senderId] = rcvdValueMsg.msgContent
                cnt += 1
        except Exception as e:
            traceback.print_exc()

    def calculateCost(self):
        # Arrays.fill(consCostList, 0.0)
        try:
            consCostList = [0.0] * (self.population)
            for neigh in self.neighbors:
                cons = self.constraints[self.edgelist[self.indexToEdge[self.agentNo][neigh]]]
                for i, pos in enumerate(self.position):
                    if neigh in self.inbox:
                        cons_calc = cons.a * math.pow(pos, 2) + cons.b * pos * self.inbox[neigh][i] + cons.c * math.pow(self.inbox[neigh][i], 2)
                        consCostList[i] += cons_calc

            self.cons_cost = consCostList
        except Exception as e:
            traceback.print_exc()

    def sendCostMessage(self):
        try:
            sumChildCost = [0.0] * (self.population)
            for baccha in self.child:
                i = 0
                while (i < self.population):
                    sumChildCost[i] += self.cons_inbox.get(baccha)[i]
                    i += 1
            sumTotalCost = [0.0] * (self.population)
            i = 0
            while (i < self.population):
                sumTotalCost[i] = sumChildCost[i] + self.cons_cost[i]
                i += 1
            neigh = self.parent
            costMsg = Message(self.agentNo, neigh, 204, sumTotalCost)
            self.mailManager[neigh].putCostMessage(costMsg)
        except Exception as e:
            traceback.print_exc()

    def receiveCostMessage(self):
        try:
            cnt = 0
            while (cnt < len(self.child)):
                rcvdCostValueMsg = self.mailManager[self.agentNo].getCostMessage()
                self.cons_inbox[rcvdCostValueMsg.senderId] = rcvdCostValueMsg.msgContent
                cnt += 1
        except Exception as e:
            traceback.print_exc()

    def sumRootChildCost(self):
        try:
            sumChildCost = [0.0] * (self.population)
            for baccha in self.child:
                if baccha in self.cons_inbox.keys():
                    for i, cons in enumerate(self.cons_inbox[baccha]):
                        sumChildCost[i] += cons
            for i, cost in enumerate(self.cons_cost):
                self.globalRootCost[i] = sumChildCost[i] + cost
                self.globalRootCost[i] /= 2
        except Exception as e:
            traceback.print_exc()

    def setPbestGbest(self):
        try:
            self.pbestParticleNo = [-1] * len(self.pbestParticleNo)
            # this.gbestParticleNo = -1;
            if (self.isMax):
                i = 0
                while (i < self.population):
                    if (self.globalRootCost[i] > self.pbest_val[i]):
                        self.pbest_val[i] = self.globalRootCost[i]
                        self.pbest_position[i] = self.position[i]
                        self.pbestParticleNo[i] = i
                    if (self.globalRootCost[i] > self.gbest_val):
                        self.gbest_val = self.globalRootCost[i]
                        self.gbest_position = self.position[i]
                        self.gbestParticleNo = i
                    i += 1
            else:
                i = 0
                while (i < self.population):
                    if (self.globalRootCost[i] < self.pbest_val[i]):
                        self.pbest_val[i] = self.globalRootCost[i]
                        self.pbest_position[i] = self.position[i]
                        self.pbestParticleNo[i] = i
                    if (self.globalRootCost[i] < self.gbest_val):
                        self.gbest_val = self.globalRootCost[i]
                        self.gbest_position = self.position[i]
                        self.gbestParticleNo = i
                    i += 1
            self.pbestParticleNo[len(self.pbestParticleNo) -
                                1] = self.gbestParticleNo
        except Exception as e:
            traceback.print_exc()

    def sendPbestGbestpositionMessage(self):
        try:
            for baccha in self.child:
                bestMsg = Message(self.agentNo, baccha, 206, self.pbestParticleNo)
                self.mailManager[baccha].putBestMessage(bestMsg)
        except Exception as e:
            traceback.print_exc()

    def receivePbestGbestPositionMessage(self):
        try:
            rcvdBestMsg = self.mailManager[self.agentNo].getBestMessage()
            self.pbestParticleNo = rcvdBestMsg.msgContent
            for i, pbest_pos in enumerate(self.pbest_position):
                if (pbest_pos == -1):
                    self.pbest_position[i] = self.position[int(self.pbestParticleNo[i])]
            if (self.gbestParticleNo == -1 or self.position[int(self.gbestParticleNo)] != self.position[int((self.pbestParticleNo[len(self.pbestParticleNo) - 1]))]):
                self.suc_cnt += 1
                self.fail_cnt = 0
            else:
                self.fail_cnt += 1
                self.suc_cnt = 0
            if len(self.pbestParticleNo) > 0 : self.gbestParticleNo = self.pbestParticleNo[-1]
            if len(self.pbestParticleNo) > 0 : self.gbest_position = self.position[int(
                (self.pbestParticleNo[-1]))]
        except Exception as e:
            traceback.print_exc()

    def printPositions(self, iteration):
        print(
            f"Position of {self.agentName} on iteration {iteration} = {' '.join(map(str, self.position))}")
