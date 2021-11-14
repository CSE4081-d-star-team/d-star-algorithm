class Node:
    def __init__(self, id):
        self.id : str = id
        # dictionary of parent node ID's
        # key = id of parent
        # value = (edge cost,)
        self.parents = {}
        # dictionary of children node ID's
        # key = id of child
        # value = (edge cost,)
        self.children = {}
        # g approximation
        self.g = float('inf')
        # rhs value
        self.rhs = float('inf')
        #Previous node when traverse
        self.previous : Node = None

        # for BFS search
        self.visited = False

    def __str__(self):
        return '' + self.id + ' g: ' + str(self.g) + ' rhs: ' + str(self.rhs)

    def __repr__(self):
        return self.__str__()

    def update_parents(self, parents):
        self.parents = parents

class GridWorld():
    def __init__(self, x_dim, y_dim, connect8=False, filepath=None):
        self.x_dim = x_dim
        self.y_dim = y_dim
        # First make an element for each row (height of grid)
        self.cells = [0] * y_dim
        # Go through each element and replace with row (width of grid)
        for i in range(y_dim):
            self.cells[i] = [0] * x_dim

        self.connect8 = connect8
        self.graph = {}
        self.goal : str = None
        self.start : str = None

        if filepath:
            self.cells, s_start, s_goal = self.parseGrid(filepath)
            #self.printGrid()
            self.generateGraphFromGrid()
            self.setGoal(s_goal)
            self.setStart(s_start)

    def __str__(self):
        msg = 'Graph:'
        for i in self.graph:
            msg += '\n  node: ' + i + ' g: ' + \
                str(self.graph[i].g) + ' rhs: ' + str(self.graph[i].rhs) + \
                ' neighbors: ' + str(self.graph[i].children)
        return msg

    def __repr__(self):
        return self.__str__()

    def printGrid(self):
        print('** GridWorld **')
        for row in self.cells:
            print(row)

    def parseGrid(self, input_file):
        '''parse text file into grid '''
        print('file', input_file)
        with open(input_file) as in_file:
            for idx, line in enumerate(in_file):
                row = [line[i] for i in range(0, len(line.strip()), 2) if line[i] != 'W']
                if row:
                    for idy in range(self.y_dim - 1):
                        # print(f'row[idy]={row[idy]}')
                        self.cells[idx-1][idy] = -1 if row[idy] == 'X' else 0
                        if row[idy] == 'R':
                            s_start = f'x{idx-1}y{idy}'
                        if row[idy] == 'G':
                            s_goal = f'x{idx-1}y{idy}'
        return self.cells, s_start, s_goal

    def setStart(self, id):
        if(self.graph[id]):
            self.start = id
        else:
            raise ValueError('start id not in graph')

    def setGoal(self, id):
        if(self.graph[id]):
            self.goal = id
        else:
            raise ValueError('goal id not in graph')

    def printGValues(self):
        for j in range(self.y_dim):
            str_msg = ""
            for i in range(self.x_dim):
                node_id = 'x' + str(i) + 'y' + str(j)
                node = self.graph[node_id]
                if node.g == float('inf'):
                    str_msg += ' - '
                else:
                    str_msg += ' ' + str(node.g) + ' '
            print(str_msg)

    def generateGraphFromGrid(self):
        edge = 1
        # print(f'dimensions of cells= {len(self.cells)} {[len(x) for x in self.cells]}')
        for i in range(len(self.cells)):
            row = self.cells[i]
            for j in range(len(row)):
                # print('graph node ' + str(i) + ',' + str(j))
                node = Node('x' + str(i) + 'y' + str(j))
                if i > 0:  # not top row
                    node.parents['x' + str(i - 1) + 'y' + str(j)] = edge
                    node.children['x' + str(i - 1) + 'y' + str(j)] = edge
                if i + 1 < self.y_dim:  # not bottom row
                    node.parents['x' + str(i + 1) + 'y' + str(j)] = edge
                    node.children['x' + str(i + 1) + 'y' + str(j)] = edge
                if j > 0:  # not left col
                    node.parents['x' + str(i) + 'y' + str(j - 1)] = edge
                    node.children['x' + str(i) + 'y' + str(j - 1)] = edge
                if j + 1 < self.x_dim:  # not right col
                    node.parents['x' + str(i) + 'y' + str(j + 1)] = edge
                    node.children['x' + str(i) + 'y' + str(j + 1)] = edge

                # store that node in the graph
                self.graph['x' + str(i) + 'y' + str(j)] = node
