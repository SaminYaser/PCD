import os
import sys
from edge import Edge
from constraint import Constraint
from parse_output import Parse_Output

class CustomParser:
    @staticmethod
    def main(args):
        parser = CustomParser()
        output = parser.getGraph()
        # print(output)

    def getGraph_sensor(self):
        MAX_NODE = 64
        path = os.path.join("benchmarks", "sensor_config_new_64.txt")
        all_nodes = []
        all_edges = []
        all_cons = []
        indexToEdge = [[0] * (MAX_NODE) for _ in range(MAX_NODE)]
        with open(path, "r") as file:
            br = file.readlines()
            for st in br:
                if st[:5] == "nodes":
                    temp = st.replace("nodes=", "", 1)
                    node_number = int(temp)
                    i = 0
                    while (i < node_number):
                        all_nodes.append(i)
                        i += 1
                if st[:5] == "edges":
                    indexToEdge = [[0] * (MAX_NODE) for _ in range(MAX_NODE)]
                    temp = st.replace("edges=", "", 1)
                    arrOfEdge = temp.split(" ", -2)
                    nums = []
                    idx = 0
                    for s in arrOfEdge:
                        anEdge = s.split(",", -2)
                        if (len(anEdge) != 2):
                            continue
                        a = int(anEdge[0])
                        b = int(anEdge[1])
                        an_edge = Edge(a, b)
                        nums.append(an_edge)
                        ulta_edge = Edge(b, a)
                        nums.append(ulta_edge)
                        indexToEdge[a][b] = idx
                        idx += 1
                        indexToEdge[b][a] = idx
                        idx += 1
                    all_edges.append(nums)
                if st[:4] == "cons":
                    temp = st.replace("cons=", "", 1)
                    arrOfCons = temp.split(">", -2)
                    cons = dict()
                    for s in arrOfCons:
                        s = s.replace("(", "")
                        s = s.replace(")", "")
                        aCons = s.split(":", -2)
                        if (len(aCons) < 2):
                            continue
                        key = aCons[0].split(",")
                        value = aCons[1].split(",")
                        a = int(key[0].strip())
                        b = int(key[1].strip())
                        c = int(value[0].strip())
                        d = int(value[1].strip())
                        r1 = int(value[2].strip())
                        r2 = int(value[3].strip())
                        r3 = int(value[4].strip())
                        r4 = int(value[5].strip())
                        #                    System.out.println("ee = "+ r1 + " " + r2 + " " + r3 + " " + r4);
                        #                    Edge an_edge = new Edge(a, b);
                        an_edge = all_edges[len(all_edges) - 1][indexToEdge[a][b]]
                        a_con = Constraint(c, d, r1, r2, r3, r4)
                        cons[an_edge] = a_con
                all_cons.append(cons)
            
        return Parse_Output(all_nodes, all_edges, all_cons)

    def getGraph(self):
        MAX_NODE = 4
        path = os.path.join("benchmarks", "example.txt")
        all_nodes = []
        all_edges = []
        all_cons = []
        indexToEdge = [[0] * (MAX_NODE) for _ in range(MAX_NODE)]
        with open(path, "r") as file:
            br = file.readlines()
            for st in br:
                if st[:5] == "nodes":
                    temp = st.replace("nodes=", "", 1)
                    node_number = int(temp)
                    i = 0
                    while (i < node_number):
                        all_nodes.append(i)
                        i += 1
                if st[:5] == "edges":
                    indexToEdge = [[0] * (MAX_NODE) for _ in range(MAX_NODE)]
                    temp = st.replace("edges=", "", 1)
                    arrOfEdge = temp.split(" ", -2)
                    nums = []
                    idx = 0
                    for s in arrOfEdge:
                        anEdge = s.split(",", -2)
                        if (len(anEdge) != 2):
                            continue
                        a = int(anEdge[0])
                        b = int(anEdge[1])
                        an_edge = Edge(a, b)
                        nums.append(an_edge)
                        ulta_edge = Edge(b, a)
                        nums.append(ulta_edge)
                        indexToEdge[a][b] = idx
                        idx += 1
                        indexToEdge[b][a] = idx
                        idx += 1
                    all_edges.append(nums)
                if st[:4] == "cons":
                    temp = st.replace("cons=", "", 1)
                    arrOfCons = temp.split(">", -2)
                    cons = dict()
                    for s in arrOfCons:
                        s = s.replace("(", "")
                        s = s.replace(")", "")
                        aCons = s.split(":", -2)
                        if (len(aCons) < 2):
                            continue
                        key = aCons[0].split(",")
                        value = aCons[1].split(",")
                        a = int(key[0].strip())
                        b = int(key[1].strip())
                        c = int(value[0].strip())
                        d = int(value[1].strip())
                        e = int(value[2].strip())
                        #                    Edge an_edge = new Edge(a, b);
                        an_edge = all_edges[len(all_edges) - 1][indexToEdge[a][b]]
                        a_con = Constraint(c, d, e)
                        # print(a_con)
                        cons[an_edge] = a_con
                    all_cons.append(cons)
        return Parse_Output(all_nodes, all_edges, all_cons)


if __name__ == "__main__":
    CustomParser.main(sys.argv)
