from queue import Queue

class Graph:
    def __init__(self, adj,  MAX_NODE=0):
        self.adj = adj
        self.MAX_NODE = MAX_NODE
        self.parent = [0] * (MAX_NODE)
        self.children = [None] * (self.MAX_NODE)
        self.neighbors = [None] * (MAX_NODE)
        self.reverse_pseudo_tree = [[0] * (self.MAX_NODE) for _ in range(self.MAX_NODE)]
        i = 0
        while (i < self.MAX_NODE):
            self.children[i] = []
            self.neighbors[i] = []
            i += 1
        self.level = [0] * (MAX_NODE)

    def bfs(self):
        visited = [False] * (self.MAX_NODE) # Arrays.fill(visited, False)
        queue = Queue()
        source = 0
        queue.put(source)
        visited[source] = True
        self.parent[source] = -1
        while not queue.empty():
            u = queue.get()
            for v in self.adj[u]:
                if not visited[v]:
                    visited[v] = True
                    self.children[u].append(v)
                    self.neighbors[u].append(v)
                    self.parent[v] = u
                    self.level[v] = self.level[u] + 1
                    queue.put(v)
                else:
                    self.neighbors[u].append(v)

    def __str__(self) -> str:
        return f"Graph children={' '.join(map(str, self.children))} neighbors={' '.join(map(str, self.neighbors))} parent={' '.join(map(str, self.parent))} level={' '.join(map(str, self.level))}"
