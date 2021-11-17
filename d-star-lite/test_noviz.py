# run profiling code for the project
# import pygame
from grid import GridWorld
from utils import stateNameToCoords, parseDims, add_reroute_obstacle
from d_star_lite import init_dstarlite, move_and_rescan
from brute_force import BruteForce
# import random
import timeit


#Testing parameters
MAX_TRIALS = 6
MAX_REROUTES = 0 # 0-9
MAX_GRIDSIZE = 100
MIN_GRIDSIZE = 50
STEP = 5


def main(gridpath, num_reroutes):
    dstar_time = 0
    brute_time = 0
    distance_traveled = 0

    # X_DIM, Y_DIM = 32, 32
    X_DIM, Y_DIM = parseDims(gridpath) # reads dynamically the size of the grid
    VIEWING_RANGE = 10 # affect the ability of the algorithm to find it's path
    rem_obstacles = num_reroutes

    # print("D* Lite Path Planning")

    # Loop until the user clicks the close button.
    done = False

    # generate graph for the grid world
    graph = GridWorld(X_DIM, Y_DIM, filepath=gridpath)
   
    s_start, s_goal = graph.start, graph.goal
    # goal_coords = stateNameToCoords(s_goal)

    graph.setStart(s_start)
    graph.setGoal(s_goal)
    k_m = 0
    # s_last = s_start
    pqueue = []

    t0 = timeit.default_timer()
    graph, pqueue, k_m = init_dstarlite(graph, pqueue, s_start, s_goal, k_m)
    t1 = timeit.default_timer()
    dstar_time += t1 - t0
    # print(f"D star init: {dstar_time}")

    
    s_current = s_start
    # pos_coords = stateNameToCoords(s_current)

    # continuous_run = False # to run without stopping
    # MAX_OBSTACLES = 10 # obstacles to be generated at random for a max number of 50 obtaacles

    # -------- Main Program Loop -----------
    while not done: 

        # move the agent with new position to go to and new k_m | actual d-star lite pathfinding
        t0 = timeit.default_timer()
        s_new, k_m = move_and_rescan(graph, pqueue, s_current, VIEWING_RANGE, k_m)
        t1 = timeit.default_timer()
        dstar_time += t1 - t0
        # print(f"Move and Rescan: {t1 - t0}")

        '''adding obstacles'''
        if rem_obstacles >= 0:
            is_success = add_reroute_obstacle(graph, s_new)
            if(is_success): 
                # print(f'{num_reroutes - rem_obstacles} reroute executed so far')
                rem_obstacles -= 1

        if s_new == 'goal':
            print('Goal Reached!')
            done = True
        else:
            # print('setting s_current to ', s_new)

            brute = BruteForce()
            t0 = timeit.default_timer()
            brute.find_path(graph, s_new)
            t1 = timeit.default_timer()
            brute_time += t1 - t0
            # print(f"brute find path: {t1 - t0}")
            # if the goal is not reached, updated current to new
            s_current = s_new
            # pos_coords = stateNameToCoords(s_current)
            # print('got pos coords: ', pos_coords)

    print(f"Brute Calc Time:{brute_time}")
    print(f"D Star Lite Calc Time: {dstar_time}")
    # print(f"Moves: {distance_traveled}")


if __name__ == "__main__":
    # path to design grid
    path = "/home/erud1t3/Desktop/AA-final-project/d-star-algorithm/d-star-lite/data"

    

    # file of increasing grid sizes
    for gridsize in range(MIN_GRIDSIZE, MAX_GRIDSIZE + 1, STEP):
        # grid are always square grids
        filepath = path + f'/grid{gridsize}.txt'
        print(f'grid of size {gridsize} at {filepath}')

        # for num_reroute in range(min(gridsize // 5, MAX_REROUTES + 1)):
            # print(f'Executing {num_reroute} obstacle caused re-routes')

        for trial in range(MAX_TRIALS + 1):
            print(f'Trial {trial}')
            main(filepath, num_reroute)
   

