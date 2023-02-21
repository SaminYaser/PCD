import random
from typing import List, Dict
from mail_manager import MailManager
from agent import Agent
from edge import Edge
from constraint import Constraint


class PFDConstrictionFactor_Agent(Agent):
    def __init__(self, mail_managers: List[MailManager], agent_no: int, neighbors: List[int], parent: int, child: List[int], population: int, domain_lb: float, domain_ub: float, max_iteration: int, is_max: bool, edge_list: List[Edge], index_to_edge: List[List[int]], constraints: Dict[Edge, Constraint], w: float, c1: float, c2: float, alpha: float) -> None:
        super().__init__(mail_managers, agent_no, neighbors, parent, child, population, domain_lb, domain_ub, max_iteration, is_max, edge_list, index_to_edge, constraints, w, c1, c2)
        self.alpha = alpha

    def update_values(self) -> None:
        ub = 1.0
        lb = 0.0
        r1 = random.uniform(lb, ub)
        r2 = random.uniform(lb, ub)

        for i in range(self.population):
            c1 = 2.05
            c2 = 2.05
            self.velocity[i] = self.alpha * (self.velocity[i] + r1 * c1 * (self.pbest_position[i] - self.position[i]) + r2 * c2 * (self.gbest_position - self.position[i]))
            self.position[i] = self.position[i] + self.velocity[i]

            if self.position[i] < self.domain_lb:
                self.position[i] = self.domain_lb
            elif self.position[i] > self.domain_ub:
                self.position[i] = self.domain_ub
