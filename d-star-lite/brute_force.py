import copy
import time

from grid import GridWorld, Node

class BruteForce:
    def __init__(self):
        self.graph = {}
        self.cell = None
        self.temp_graph = None
        self.list = []

    #Coordination - key = f'x{idx}y{idy}' : value = Node
    #new list has different reference with original grid
    # but shares the same cell information for obstacles
    def find_path(self, grid : GridWorld, current_pos : str):
        #copies only the value
        self.temp_grid = copy.deepcopy(grid)
        current_node : Node = self.temp_grid.graph[current_pos]

        self.list.append(current_node)
        distance = 0
        while (len(self.list) != 0):
            result : Node = self.breadth_first_search()
            if result != None:
                break
        distance = 0

        while (result != None):
            # print("Taking Previous " + str(result.id))    
            distance += 1
            if (result.id == current_pos):
                break
            result = result.previous
        
        
        # print(distance)

    #Look for the goal using BFS
    def breadth_first_search(self):        
        current_node : Node = self.list.pop(0)
        x, y = self.get_cooridnation(current_node)
        
        if current_node.id == self.temp_grid.goal:   #Goal
            current_node.visited = True
            return current_node
        elif current_node.visited:                   #Visited
            return None
        elif self.temp_grid.cells[y][x] == -1:       #Obstaccles
            current_node.visited = True
            return None

        current_node.visited = True
        #Recursive case
        next_node = self.go_up(x, y, current_node)        #UP
        if next_node != None and not next_node.visited:
            # print(str(current_node.id) + " - Going up")
            self.list.append(next_node)

        next_node = self.go_down(x, y, current_node)      #DOWN
        if next_node != None and not next_node.visited:
            # print(str(current_node.id) + " - Going down")
            self.list.append(next_node)

        next_node = self.go_left(x, y, current_node)      #LEFT
        if next_node != None:
            # print(str(current_node.id) + " - Going left")
            self.list.append(next_node)

        next_node = self.go_right(x, y, current_node)     #RIGHT
        if next_node != None and not next_node.visited:
            # print(str(current_node.id) + " - Going right")
            self.list.append(next_node)

        return None

    def get_cooridnation(self, node : Node):
        id = node.id
        id = id.replace("x", " ")
        id = id.replace("y", " ")
        list = id.split(' ')
        list.remove('')
        current_x = int(list[0])
        current_y = int(list[1])
        return current_x, current_y

    def get_dic_key(self, x, y):
        return f'x{x}y{y}'

    def to_node(self, coord : str):
        return self.temp_grid.graph[coord]

    def go_up(self, x, y, current_node):
        if y == 0:
            return None
        else:
            temp_node : Node = self.to_node(f'x{x}y{y - 1}')
            if temp_node.previous == None:
                temp_node.previous = current_node
            return temp_node

    def go_down(self, x, y, current_node):
        if y == self.temp_grid.y_dim - 1:
            return None
        else:
            temp_node : Node = self.to_node(f'x{x}y{y + 1}')
            if temp_node.previous == None:
                temp_node.previous = current_node
            return temp_node
    
    def go_left(self, x, y, current_node):
        if x == 0:
            return None
        else:
            temp_node : Node = self.to_node(f'x{x - 1}y{y}')
            if temp_node.previous == None:
                temp_node.previous = current_node
            return temp_node
    
    def go_right(self, x, y, current_node):
        if x == self.temp_grid.x_dim - 1:
            return None
        else:
            temp_node : Node = self.to_node(f'x{x + 1}y{y}')
            if temp_node.previous == None:
                temp_node.previous = current_node
            return temp_node
