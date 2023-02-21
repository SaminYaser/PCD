import sys
from typing import Dict, List
from edge import Edge
from constraint import Constraint
from problem import Problem

class Main:
    @staticmethod
    def cost_calc(constraints: Dict[Edge, Constraint], edgelist: List[Edge]) -> float:
        sum = 0.0

        for e in edgelist:
            x = 0.6418937344000017
            y = 0.6418937344000017

            cons = constraints[e]
            a = cons.a
            b = cons.b
            c = cons.c

            if e.node1 == 0:
                x = 0.6418937344000017
            elif e.node2 == 0:
                y = 0.6418937344000017

            sum += a * x ** 2 + b * (x) * (y) + c * y ** 2

        return sum / 2.0

    @staticmethod
    def main(args: List[str]) -> None:
        # problem_name = args[0]
        # problem = int(problem_name)

        MAX_SAME_PROB = 1
        MAX_DIFF_PROB = 2
        MAX_NODE = 4
        w = 0.72
        c1 = 1.49
        c2 = 1.49
        p1 = Problem(0, 0, MAX_SAME_PROB, MAX_DIFF_PROB, MAX_NODE, w, c1, c2)
        p1.newProblem()

if __name__ == '__main__':
    Main.main(sys.argv[1:])
