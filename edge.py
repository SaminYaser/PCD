class Edge():
    def __init__(self, node1: int = 0,  node2: int = 0):
        self.node1 = node1
        self.node2 = node2

    def __str__(self) -> str:
        return f"Edge node1={self.node1} node2={self.node2}"
