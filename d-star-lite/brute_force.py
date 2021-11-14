from grid import GridWorld, Node

class BruteForce:
    #BFS?
    #Coordination - key = f'x{idx}y{idy}' : value = Node
    def findPath(grid : GridWorld, start : Node, end : Node):
        # connects the current row then connects current row to previous row
        for y in range(grid.y_dim):
            for x in range(grid.x_dim):
                pass
                print(grid.cells[y][x], end = '\n')
                print(str(grid.graph[f'x{x}y{y}']) + ", ", end = '\n')
            print("")
