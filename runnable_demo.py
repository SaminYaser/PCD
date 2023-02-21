from typing import List, Tuple, Dict
import multiprocessing
from collections import defaultdict
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from agent import Agent
from crossover_agent import CrossOverAgent
from mail_manager import MailManager
from edge import Edge
from constraint import Constraint
from pfd_cognition_only_agent import PFDCognitionOnly_Agent
from pfd_constriction_factor_agent import PFDConstrictionFactor_Agent
from pfd_dsa_agent import PFDDSA_Agent
from pfd_social_only_agent import PFDSocialOnly_Agent
# from problem import Problem
import time
import os

class RunnableDemo(Thread):
    def __init__(self, problem, agentType: str, mailManagers: List[MailManager], threadNo: int, name: str, maxIteration: int,
                 neighbors: List[int], parent: int, child: List[int], population: int, domain_lb: float, domain_ub: float,
                 isMax: bool, edgelist: List[Edge], indexToEdge: List[List[int]], constraints: Dict[Edge, Constraint],
                 w: float, c1: float, c2: float):
        super().__init__()
        self.problem = problem
        self.threadNo = threadNo
        self.threadName = name
        self.maxIteration = maxIteration
        self.currentIter = 0
        self.mailManagers = mailManagers
        self.timeResults: Dict[str, int] = {}
        self.iterTimeResults: Dict[int, List[int]] = defaultdict(list)
        self.simTimeArray: List[int] = []
        self.iterSol: List[float] = []
        self.runTimeArray: List[int] = []

        self.bp = [0.0] * population
        if agentType == "PFD":
            self.agent = Agent(mailManagers, threadNo, neighbors, parent, child, population, domain_lb, domain_ub,
                               maxIteration, isMax, edgelist, indexToEdge, constraints, w, c1, c2)
        elif agentType == "PFDDSA":
            self.agent = PFDDSA_Agent(mailManagers, threadNo, neighbors, parent, child, population, domain_lb, domain_ub,
                                      maxIteration, isMax, edgelist, indexToEdge, constraints, w, c1, c2)
        elif agentType == "ConsPFD":
            self.agent = PFDConstrictionFactor_Agent(mailManagers, threadNo, neighbors, parent, child, population,
                                                     domain_lb, domain_ub, maxIteration, isMax, edgelist, indexToEdge,
                                                     constraints, w, c1, c2, self.setParam())
        elif agentType == "CrossOverAgent":
            self.agent = CrossOverAgent(mailManagers, threadNo, neighbors, parent, child, population, domain_lb,
                                        domain_ub, maxIteration, isMax, edgelist, indexToEdge, constraints, w, c1, c2,
                                        self.initBP(population))
        elif agentType == "CognitionOnly":
            self.agent = PFDCognitionOnly_Agent(mailManagers, threadNo, neighbors, parent, child, population, domain_lb,
                                                domain_ub, maxIteration, isMax, edgelist, indexToEdge, constraints, w,
                                                c1, c2)
        elif agentType == "SocialOnly":
            self.agent = PFDSocialOnly_Agent(mailManagers, threadNo, neighbors, parent, child, population, domain_lb,
                                             domain_ub, maxIteration, isMax, edgelist, indexToEdge, constraints, w, c1,
                                             c2)

    def var_to_coordinate(self, agent_id: int, lb: float, ub: float) -> List[float]:
        col = 8
        x = agent_id // col
        y = agent_id % col

        domain_lbx  = lb + x * 5 + ub * x
        domain_ubx = ub + x * 5 + ub * x

        domain_lby = lb + y * 5 + ub * y
        domain_uby = ub + y * 5 + ub * y

        domains = [domain_lbx, domain_ubx, domain_lby, domain_uby]
        return domains

    def setParam(self) -> float:
        K = 0.8
        phi = 4.1
        chiX = 2*K / (phi-2+pow(phi, 2)-4*phi)**0.5
        alpha = (1 + chiX * (phi-2)) / (phi-1)
        return alpha

    def initBP(self, population: int) -> List[float]:
        self.bp = [1/population for i in range(population)]
        return self.bp

    def run(self):
        # print("Running", self.threadName)
        try:
            start = time.process_time()

            while self.agent.currentIter < self.agent.maxIteration:
                self.agent.getMailManager()[0].startNewIter()
                wmax = 1.4
                wmin = 0.4
                decreasingW = wmax - (wmax - wmin) * (self.agent.currentIter / self.agent.maxIteration)
                self.agent.w = decreasingW

                if self.agent.currentIter == 0:
                    self.agent.initValues()
                else:
                    self.agent.updateValues()

                self.agent.sendValueMessage()
                self.agent.receiveValueMessage()
                self.agent.calculateCost()

                self.agent.receiveCostMessage()
                if self.threadNo != 0:
                    self.agent.sendCostMessage()
                    self.agent.receivePbestGbestPositionMessage()
                    self.agent.sendPbestGbestpositionMessage()
                else:
                    self.agent.sumRootChildCost()
                    self.agent.setPbestGbest()
                    self.agent.sendPbestGbestpositionMessage()

                if self.threadNo == 0:
                    print("Iteration", self.agent.currentIter, "gbest val", self.agent.gbest_val)
                    endTime = time.time()
                    diff = endTime - self.agent.starttime
                    iterEnd = time.process_time()
                    iterDiffInMillis = (iterEnd - start) * 1000
                    self.simTimeArray.append(iterDiffInMillis)
                    self.runTimeArray.append(diff)
                    self.iterTimeResults[self.threadNo] = self.simTimeArray
                    self.iterSol.append(self.agent.gbest_val)

                self.agent.getMailManager()[0].makeTrue(self.threadNo)
                self.agent.getMailManager()[0].checkAllTrue(self.threadNo)
                self.agent.currentIter += 1

                if self.agent.currentIter == 9:
                    print("agent", self.agent.agentNo, "pos =", self.agent.gbest_position)

                time.sleep(0.05)

        except Exception as e:
            print("Thread", self.threadName, "interrupted.", e)
            import traceback
            traceback.print_exc()
            os._exit(1)

        if self.threadNo == 0:
            # arrayNo = self.problem.problemNo * self.problem.MAX_SAME_Problem + self.problem.sameProbIt

            same_it = self.problem.sameProbIt + 1
            try:
                if same_it < self.problem.MAX_SAME_Problem:
                    self.problem.setSameProbIt(same_it)
                    self.problem.newProblem()
                else:
                    diff_it = self.problem.problemNo + 1
                    if diff_it < self.problem.MAX_DIFF_PROB:
                        self.problem.setSameProbIt(0)
                        self.problem.setProblemNo(diff_it)
                        self.problem.newProblem()
                    else:
                        print("DONEEEEE")
            except Exception as e:
                print("Exception while creating new problem", e)
                os._exit(1)

