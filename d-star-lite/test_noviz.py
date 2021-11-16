# run profiling code for the project
# import pygame
from grid import GridWorld
from utils import stateNameToCoords, parseDims
from d_star_lite import init_dstarlite, move_and_rescan
from brute_force import BruteForce
# import random

# path to design grid
filep = "C:\\Users\\the_3\\Desktop\\AA\\testCaseGenerator\\data\\output.txt"

# Initialize pygame
# pygame.init()

# X_DIM, Y_DIM = 32, 32
X_DIM, Y_DIM = parseDims(filep) # reads dynamically the size of the grid
VIEWING_RANGE = 10 # affect the ability of the algorithm to find it's path


# Set title of screen
# pygame.display.set_caption("D* Lite Path Planning")
print("D* Lite Path Planning")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
# clock = pygame.time.Clock()



if __name__ == "__main__":

    # generate graph for the grid world
    graph = GridWorld(X_DIM, Y_DIM, filepath=filep)
    # s_start = 'x1y2' # [1, 2]

    # generate starting point
    # s_start = f'x{random.randint(0, X_DIM)}y{random.randint(0, Y_DIM)}'
    # s_goal = 'x5y4'  # [5, 4]

    # generate ending point
    # s_goal = f'x{random.randint(0, X_DIM)}y{random.randint(0, Y_DIM)}'
    s_start, s_goal = graph.start, graph.goal
    goal_coords = stateNameToCoords(s_goal)

    graph.setStart(s_start)
    graph.setGoal(s_goal)
    k_m = 0
    s_last = s_start
    pqueue = []

    graph, pqueue, k_m = init_dstarlite(graph, pqueue, s_start, s_goal, k_m)

    s_current = s_start
    pos_coords = stateNameToCoords(s_current)

    # continuous_run = False # to run without stopping
    # MAX_OBSTACLES = 10 # obstacles to be generated at random for a max number of 50 obtaacles

    # -------- Main Program Loop -----------
    while not done: 
        # if continuous_run: 
            # move the agent with new position to go to and new k_m | actual d-star lite pathfinding
        s_new, k_m = move_and_rescan(graph, pqueue, s_current, VIEWING_RANGE, k_m)

        if s_new == 'goal':
            print('Goal Reached!')
            done = True
        else:
            print('setting s_current to ', s_new)
            # if the goal is not reached, updated current to new
            s_current = s_new
            pos_coords = stateNameToCoords(s_current)
            # print('got pos coords: ', pos_coords)

        '''adding obstacles'''
        # add_obstacles()