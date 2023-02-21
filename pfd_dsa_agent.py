import random
from typing import List, Tuple, Dict
from agent import Agent
from mail_manager import MailManager
from constraint import Constraint
from edge import Edge


class PFDDSA_Agent(Agent):
    def __init__(self, mailManager: List[MailManager], AgentNo: int, neighbors: List[int], parent: int, child: List[int], population: int, domain_lb: float, domain_ub: float, maxIteration: int, ismax: bool, edgelist: List[Edge], indexToEdge: List[List[int]], constraints: Dict[Edge, Constraint], w: float, c1: float, c2: float):
        super().__init__(mailManager, AgentNo, neighbors, parent, child, population, domain_lb,
                         domain_ub, maxIteration, ismax, edgelist, indexToEdge, constraints, w, c1, c2)
        self.neighbors = neighbors

    def updateValues(self):
        threshold = 10
        if self.currentIter % threshold == 0:
            self.runDSA()
        else:
            self.PFDUpdate()

    def PFDUpdate(self):
        ub = 1.0
        lb = 0.0
        r1 = (random.random() * (ub - lb)) + lb
        r2 = (random.random() * (ub - lb)) + lb
        for i in range(self.population):
            if i == self.gbestParticleNo:
                self.velocity[i] = -self.position[i] + self.gbest_position + \
                    (self.w * self.velocity[i]) + \
                    self.cal_row() * (1 - (2 * r2))
                self.position[i] = self.position[i] + self.velocity[i]
            else:
                self.velocity[i] = self.w * self.velocity[i] + self.c1 * r1 * (
                    self.pbest_position[i] - self.position[i]) + self.c2 * r2 * (self.gbest_position - self.position[i])
                self.position[i] = self.position[i] + self.velocity[i]
            if self.position[i] < self.domain_lb:
                self.position[i] = self.domain_lb
            elif self.position[i] > self.domain_ub:
                self.position[i] = self.domain_ub

    # def runDSA(self):
    #     for i in range(self.population):
    #         A = 0
    #         B = 0
    #         for neigh in self.neighbors:
    #             cons = self.constraints[self.edgelist[self.indexToEdge[self.agentNo][neigh]]]
    #             A += cons.getA()
    #             B += cons.getB() * self.inbox[neigh][i]
    #         if A != 0:
    #             mid = -B / (2 * A)
    #         else:
    #             mid = (self.domain_lb + self.domain_ub) / 2.0
    #         cons_calc_lb = 0
    #         cons_calc_ub = 0
    #         cons_calc_mid = 0
    #         if self.isMax:
    #             temp_cost = float('-inf')
    #         else:
    #             temp_cost = float('inf')
    #         for neigh in self.neighbors:
    #             cons = self.constraints[self.edgelist[self.indexToEdge[self.agentNo][neigh]]]
    #             cons_calc_lb += cons.getA() * (self.domain_lb ** 2) + cons.getB() * self.domain_lb * self.inbox[neigh][i] + cons.getC() * (self.inbox[neigh][i] ** 2)
    #             cons_calc_ub += cons.getA() * (self.domain_ub ** 2) + cons.getB() * self.domain_ub * self.inbox[neigh][i] +
    def runDSA(self):
        A, B, C = 0, 0, 0
        mid = 0

        for i in range(self.population):

            for neigh in self.neighbors:
                cons = self.constraints[self.edgelist[self.indexToEdge[self.agentNo][neigh]]]
                A += cons.a
                B += cons.b * self.inbox[neigh][i]
            if A != 0:
                mid = -B/(2*A)
            else:
                mid = (self.domain_lb + self.domain_ub) / 2.0
            cons_calc_lb, cons_calc_ub, cons_calc_mid = 0, 0, 0

            temp_cost, temp = 0, 0
            if self.isMax:
                temp_cost = -float('inf')
            else:
                temp_cost = float('inf')
            for neigh in self.neighbors:
                cons = self.constraints[self.edgelist[self.indexToEdge[self.agentNo][neigh]]]
                cons_calc_lb += cons.a * pow(self.domain_lb, 2) + cons.b * self.domain_lb * \
                    self.inbox[neigh][i] + \
                    cons.c * pow(self.inbox[neigh][i], 2)
                cons_calc_ub += cons.a * pow(self.domain_ub, 2) + cons.b * self.domain_ub * \
                    self.inbox[neigh][i] + \
                    cons.c * pow(self.inbox[neigh][i], 2)

                if mid >= self.domain_lb and mid <= self.domain_ub:
                    cons_calc_mid += cons.a * pow(mid, 2) + cons.b * mid * \
                        self.inbox[neigh][i] + \
                        cons.c * pow(self.inbox[neigh][i], 2)

                else:
                    if self.isMax:
                        cons_calc_mid = -float('inf')
                    else:
                        cons_calc_mid = float('inf')

            if self.isMax:
                if cons_calc_mid >= cons_calc_lb and cons_calc_mid >= cons_calc_ub:
                    temp_cost = cons_calc_mid
                    temp = mid
                elif cons_calc_lb >= cons_calc_mid and cons_calc_lb >= cons_calc_ub:
                    temp_cost = cons_calc_lb
                    temp = self.domain_lb

                elif cons_calc_ub >= cons_calc_mid and cons_calc_ub >= cons_calc_lb:
                    temp_cost = cons_calc_ub
                    temp = self.domain_ub

                if temp_cost > self.cons_cost[i] and random.random() < self.dsa_prob:
                    self.position[i] = temp
            else:
                if cons_calc_mid <= cons_calc_lb and cons_calc_mid <= cons_calc_ub:
                    temp_cost = cons_calc_mid
                    temp = mid
                elif cons_calc_lb <= cons_calc_mid and cons_calc_lb <= cons_calc_ub:
                    temp_cost = cons_calc_lb
                    temp = self.domain_lb

                elif cons_calc_ub <= cons_calc_mid and cons_calc_ub <= cons_calc_lb:
                    temp_cost = cons_calc_ub
                    temp = self.domain_ub

                if temp_cost < self.cons_cost[i] and random.random() < self.dsa_prob:
                    self.position[i] = temp
