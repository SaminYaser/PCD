from threading import Thread
from custom_parser import CustomParser

from graph import Graph
from mail_manager import MailManager
from runnable_demo import RunnableDemo


class Problem:
    def __init__(
        self,
        problemNo: int,
        sameProbIt: int,
        MAX_SAME_PROB: int,
        MAX_DIFF_PROB: int,
        MAX_NODE: int,
        w: float,
        c1: float,
        c2: float
    ) -> None:
        self.problemNo = problemNo
        self.sameProbIt = sameProbIt
        self.MAX_SAME_Problem = MAX_SAME_PROB
        self.MAX_DIFF_PROB = MAX_DIFF_PROB
        self.MAX_NODE = MAX_NODE
        self.w = w
        self.c1 = c1
        self.c2 = c2

    def setSameProbIt(self, sameProbIt: int) -> None:
        self.sameProbIt = sameProbIt

    def setProblemNo(self, problemNo: int) -> None:
        self.problemNo = problemNo

    def newProblem(self) -> None:
        # System.out.println("Problem " + problemNo +" same prob it = " + sameProbIt);
        parser = CustomParser()
        output = parser.getGraph()

        R = [None] * self.MAX_NODE
        adj = [[] for _ in range(self.MAX_NODE)]
        indexToEdge = [[0] * self.MAX_NODE for _ in range(self.MAX_NODE)]

        edgelist = output.all_edges[self.problemNo]

        for i in range(self.MAX_NODE):
            adj[i] = []

        idx = 0
        for e in edgelist:
            u = e.node1
            v = e.node2
            indexToEdge[u][v] = idx
            idx += 1
            adj[u].append(v)

        graph = Graph(adj, self.MAX_NODE)
        print(graph)
        graph.bfs()
        print(graph)

        mailManager = [None] * self.MAX_NODE

        for j in range(self.MAX_NODE):
            mailManager[j] = MailManager(
                len(graph.neighbors[j]),
                self.MAX_NODE
            )
            mailManager[j].start()
        for i in range(self.MAX_NODE):
            R[i] = RunnableDemo(
                self,
                "PFD",
                mailManager,
                i,
                "Agent-" + str(i),
                20,
                graph.neighbors[i],
                graph.parent[i],
                graph.children[i],
                100,
                -10,
                10,
                False,
                edgelist,
                indexToEdge,
                output.all_cons[self.problemNo],
                self.w,
                self.c1,
                self.c2
            )
            R[i].start()
