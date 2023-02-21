from typing import Dict, List
from edge import Edge
from constraint import Constraint


class Parse_Output:
    def __init__(self, all_nodes: List[int],  all_edges: List[List[Edge]],  all_cons: List[Dict[Edge, Constraint]]):
        self.all_nodes = all_nodes
        self.all_edges = all_edges
        self.all_cons = all_cons

    def __str__(self) -> str:
        return f"Parse_Output all_nodes={self.all_nodes} all_edges={self.all_edges} all_cons={self.all_cons}"
