from typing import List, Tuple
import random
from constraint import Constraint
from agent import Agent
from edge import Edge


class PFDSocialOnly_Agent(Agent):
    def __init__(self, mailManager: List, AgentNo: int, neighbors: List[int], parent: int, child: List[int], population: int, domain_lb: float, domain_ub: float, maxIteration: int, ismax: bool, edgelist: List[Edge], indexToEdge: List[List[int]], constraints: List[Constraint], w: float, c1: float, c2: float) -> None:
        super().__init__(mailManager, AgentNo, neighbors, parent, child, population, domain_lb,
                         domain_ub, maxIteration, ismax, edgelist, indexToEdge, constraints, w, c1, c2)

    def updateValues(self) -> None:
        ub = 1.0
        lb = 0.0
        r1 = random.uniform(lb, ub)
        r2 = random.uniform(lb, ub)

        for i in range(self.population):
            if i == self.gbestParticleNo:
                self.velocity[i] = -self.position[i] + self.gbest_position + \
                    (self.w * self.velocity[i]) + \
                    self.cal_row() * (1 - (2 * r2))
                self.position[i] = self.position[i] + self.velocity[i]
            else:
                self.velocity[i] = self.w * self.velocity[i] + \
                    self.c2 * r2 * (self.gbest_position - self.position[i])
                self.position[i] = self.position[i] + self.velocity[i]

            if self.position[i] < self.domain_lb:
                self.position[i] = self.domain_lb
            elif self.position[i] > self.domain_ub:
                self.position[i] = self.domain_ub
