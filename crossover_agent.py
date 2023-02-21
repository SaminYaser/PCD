import math
import random
from typing import List
from agent import Agent
from constraint import Constraint
from edge import Edge
from mail_manager import MailManager

class CrossOverAgent(Agent):
    def setBp(self, bp):
        self.bp = bp
    bp = None

    def __init__(self, mailManager: List[MailManager],  AgentNo,  neighbors,  parent,  child,  population,  domain_lb,  domain_ub,  maxIteration,  ismax,  edgelist,  indexToEdge,  constraints,  w,  c1,  c2,  bp):
        super().__init__(mailManager,  AgentNo,  neighbors,  parent,  child,  population,  domain_lb,  domain_ub,  maxIteration,  ismax,  edgelist,  indexToEdge,  constraints,  w,  c1,  c2)
        self.bp = bp

    def calcBPProb(self):
        costSum = 0
        i = 0
        while (i < self.population):
            costSum += abs(self.cons_cost[i])
            i += 1
        i = 0
        while (i < self.population):
            self.bp[i] = abs(self.cons_cost[i]) / costSum
            i += 1

    def randomgen(self):
        if (self.currentIter != 0):
            self.calcBPProb()
        totalWeight = 0.0
        for prob in self.bp:
            totalWeight += prob
        # Now choose a random item
        randomIndex = 0
        rand = random.random() * totalWeight
        i = 0
        while (i < len(self.bp)):
            rand -= self.bp[i]
            if (rand <= 0.0):
                randomIndex = i
                break
            i += 1
        return randomIndex

    def calcBPProb_maxfirst(self):
        bestCost = 1.7976931348623157E308
        worstCost = 4.9E-324
        i = 0
        while (i < self.population):
            if (self.cons_cost[i] < bestCost):
                bestCost = self.cons_cost[i]
            if (self.cons_cost[i] > worstCost):
                worstCost = self.cons_cost[i]
            i += 1
        rankSum = 0
        rankList = [0.0] * (self.population)
        i = 0
        while (i < self.population):
            rank = (self.cons_cost[i] - bestCost + 1) / \
                (worstCost - bestCost + 1)
            rankList[i] = rank
            rankSum += rank
            i += 1
        i = 0
        while (i < self.population):
            self.bp[i] = rankList[i] / rankSum
            i += 1

    def calcBPProb_minfirst(self):
        costSum = 0
        bestCost = 1.7976931348623157E308
        worstCost = 4.9E-324
        i = 0
        while (i < self.population):
            if (self.cons_cost[i] < bestCost):
                bestCost = self.cons_cost[i]
            if (self.cons_cost[i] > worstCost):
                worstCost = self.cons_cost[i]
            costSum += self.cons_cost[i]
            i += 1
        rankSum = 0
        rankList = [0.0] * (self.population)
        i = 0
        while (i < self.population):
            rank = (
                worstCost - self.cons_cost[i] + 1) / (worstCost - bestCost + 1)
            rankList[i] = rank
            rankSum += rank
            i += 1
        i = 0
        while (i < self.population):
            self.bp[i] = rankList[i] / rankSum
            i += 1

    def setParam(self):
        K = 0.8
        phi = 4.1
        chiX = 2 * K / (phi - 2 + math.sqrt(math.pow(phi, 2) - 4 * phi))
        alpha = (1 + chiX * (phi - 2)) / (phi - 1)
        return alpha

    def updateValues(self):
        ub = 1.0
        lb = 0.0
        r1 = (random.random() * (ub - lb)) + lb
        r2 = (random.random() * (ub - lb)) + lb
        selectedPar1 = self.randomgen()
        selectedPar2 = self.randomgen()
        i = 0
        while (i < self.population):
            if (i == selectedPar1):
                self.position[i] = r1 * self.position[i] + \
                    (1.0 - r1) * self.position[selectedPar2]
                nom = (
                    self.velocity[i] + self.velocity[selectedPar2]) * self.velocity[selectedPar2]
                deNom = abs(self.velocity[i] + self.velocity[selectedPar2])
                if (deNom == 0 or self.velocity[i] == 0):
                    if (i == self.gbestParticleNo):
                        self.velocity[i] = -self.position[i] + self.gbest_position + \
                            (self.w * self.velocity[i]) + \
                            self.cal_row() * (1 - (2 * r2))
                    else:
                        self.velocity[i] = self.w * self.velocity[i] + self.c1 * r1 * (
                            self.pbest_position[i] - self.position[i]) + self.c2 * r2 * (self.gbest_position - self.position[i])
                else:
                    self.velocity[i] = nom / deNom
            elif (i == selectedPar2):
                self.position[i] = r1 * self.position[i] + \
                    (1.0 - r1) * self.position[selectedPar1]
                nom = (
                    self.velocity[i] + self.velocity[selectedPar1]) * self.velocity[selectedPar1]
                deNom = abs(self.velocity[i] + self.velocity[selectedPar1])
                if (deNom == 0):
                    if (i == self.gbestParticleNo):
                        self.velocity[i] = -self.position[i] + self.gbest_position + \
                            (self.w * self.velocity[i]) + \
                            self.cal_row() * (1 - (2 * r2))
                    else:
                        self.velocity[i] = self.w * self.velocity[i] + self.c1 * r1 * (
                            self.pbest_position[i] - self.position[i]) + self.c2 * r2 * (self.gbest_position - self.position[i])
                else:
                    self.velocity[i] = nom / deNom
            else:
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
            elif (self.position[i] > self.domain_ub):
                self.position[i] = self.domain_ub
            i += 1
