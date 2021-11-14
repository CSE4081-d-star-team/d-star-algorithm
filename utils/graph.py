import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, v_type):
        self.v_type = v_type
        self.adjacent = []  # ordered by up left down right
        self.visited = False
        self.is_obstacle = (v_type == 'X')

    # adds edge from self to vertice
    def add_adj(self, vertex):
        self.adjacent.append(vertex)
        if len(self.adjacent) == 4:
            self.reorder_adj()

    # gets adjacent from index
    def get_adj(self, index):
        return self.adjacent[index]

    # reorders after all adj are added, changes adj u l r d to u l d r (swap d and r)
    def reorder_adj(self):
        self.adjacent[2], self.adjacent[3] = self.adjacent[3], self.adjacent[2]


class Graph:
    save_graph_num = 1
    
    def __init__(self):
        self.start = None
        self.goal = None
        self.root = None

    def connect_vertices(self, vertex1, vertex2):
        # vertex1 on left/above vertice2 on right/below
        if vertex1 is not None:
            vertex1.add_adj(vertex2)
        if vertex2 is not None:
            vertex2.add_adj(vertex1)

    def find_r_or_g(self, c, vertex):
        if c == 'R':
            self.start = vertex
        elif c == 'G':
            self.goal = vertex

    def __str__(self):
        msg = ""
        y_vertex = self.root
        while y_vertex is not None:
            x_vertex = y_vertex
            while x_vertex is not None:
                msg += f"{x_vertex.v_type}"
                x_vertex = x_vertex.get_adj(3)
            msg += '\n'
            y_vertex = y_vertex.get_adj(2)
        return msg
