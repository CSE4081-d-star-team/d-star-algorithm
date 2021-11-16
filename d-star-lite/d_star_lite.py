import heapq
from utils import stateNameToCoords


def top_key(queue):
    queue.sort()
    # print(queue)
    if len(queue) > 0:
        return queue[0][:2]
    else:
        # print('empty queue!')
        return (float('inf'), float('inf'))


def heuristic_from_s(id, s):
    x_distance = abs(int(id.split('x')[1][0]) - int(s.split('x')[1][0]))
    y_distance = abs(int(id.split('y')[1][0]) - int(s.split('y')[1][0]))
    return max(x_distance, y_distance)


def calculate_key(grid, id, s_current, k_m):
    key1 = min(grid.graph[id].g, grid.graph[id].rhs) \
            + heuristic_from_s(id, s_current) \
            + k_m # key 1 
    key2 = min(grid.graph[id].g, grid.graph[id].rhs) # key 2
    return (key1, key2)


def update_vertex(graph, queue, id, s_current, k_m):
    s_goal = graph.goal
    if id != s_goal:
        min_rhs = float('inf')
        for i in graph.graph[id].children:
            min_rhs = min(
                min_rhs, graph.graph[i].g + graph.graph[id].children[i])
        graph.graph[id].rhs = min_rhs
    id_in_queue = [item for item in queue if id in item]
    if id_in_queue != []:
        if len(id_in_queue) != 1:
            raise ValueError('more than one ' + id + ' in the queue!')
        queue.remove(id_in_queue[0])
    if graph.graph[id].rhs != graph.graph[id].g:
        heapq.heappush(queue, calculate_key(graph, id, s_current, k_m) + (id,))


def compute_shortest_path(graph, queue, s_start, k_m):
    while (graph.graph[s_start].rhs != graph.graph[s_start].g) or \
        (top_key(queue) < calculate_key(graph, s_start, s_start, k_m)):
       
        k_old = top_key(queue)
        u = heapq.heappop(queue)[2]
        if k_old < calculate_key(graph, u, s_start, k_m):
            heapq.heappush(queue, calculate_key(graph, u, s_start, k_m) + (u,))
        elif graph.graph[u].g > graph.graph[u].rhs:
            graph.graph[u].g = graph.graph[u].rhs
            for i in graph.graph[u].children:
                update_vertex(graph, queue, i, s_start, k_m)
        else:
            graph.graph[u].g = float('inf')
            update_vertex(graph, queue, u, s_start, k_m)
            for i in graph.graph[u].children:
                update_vertex(graph, queue, i, s_start, k_m)
        # graph.printGValues()


def next_in_shortest_path(graph, s_current):
    min_rhs = float('inf')
    s_next = None
    if graph.graph[s_current].rhs == float('inf'):
        print('You are done stuck')
    else:
        for i in graph.graph[s_current].children:
            # print(i)
            child_cost = graph.graph[i].g + graph.graph[s_current].children[i]
            # print(child_cost)
            if (child_cost) < min_rhs:
                min_rhs = child_cost
                s_next = i
        if s_next:
            return s_next
        else:
            raise ValueError('could not find child for transition!')


def scan_obstacles(graph, queue, s_current, scan_range, k_m):
    states_to_update = {}
    range_checked = 0
    if scan_range >= 1:
        for neighbor in graph.graph[s_current].children:
            neighbor_coords = stateNameToCoords(neighbor)
            states_to_update[neighbor] = graph.cells[neighbor_coords[1]][neighbor_coords[0]]
        range_checked = 1
    # print(states_to_update)

    while range_checked < scan_range:
        new_set = {}
        for state in states_to_update:
            new_set[state] = states_to_update[state]
            for neighbor in graph.graph[state].children:
                if neighbor not in new_set:
                    neighbor_coords = stateNameToCoords(neighbor)
                    new_set[neighbor] = graph.cells[neighbor_coords[1]][neighbor_coords[0]]
        range_checked += 1
        states_to_update = new_set

    new_obstacle = False
    for state in states_to_update:
        if states_to_update[state] < 0:  # found cell with obstacle
            # print('found obstacle in ', state)
            for neighbor in graph.graph[state].children:
                # first time to observe this obstacle where one wasn't before
                if(graph.graph[state].children[neighbor] != float('inf')):
                    neighbor_coords = stateNameToCoords(state)
                    graph.cells[neighbor_coords[1]][neighbor_coords[0]] = -2
                    graph.graph[neighbor].children[state] = float('inf')
                    graph.graph[state].children[neighbor] = float('inf')
                    update_vertex(graph, queue, state, s_current, k_m)
                    new_obstacle = True
        # elif states_to_update[state] == 0: #cell without obstacle
            # for neighbor in graph.graph[state].children:
                # if(graph.graph[state].children[neighbor] != float('inf')):

    # print(graph)
    return new_obstacle


def move_and_rescan(graph, queue, s_current, scan_range, k_m):
    if(s_current == graph.goal):
        return 'goal', k_m
    else:
        s_last = s_current
        s_new = next_in_shortest_path(graph, s_current)
        if not s_new:
            # s_new = s_last # to return to previous spot and wait
            print('No path to goal can be found :(((')
            quit() # quit since the goal cannot be found
        new_coords = stateNameToCoords(s_new)

        if(graph.cells[new_coords[1]][new_coords[0]] == -1):  # just ran into new obstacle
            s_new = s_current  # need to hold tight and scan/replan first

        results = scan_obstacles(graph, queue, s_new, scan_range, k_m)
        # print(graph)
        k_m += heuristic_from_s(s_last, s_new)
        compute_shortest_path(graph, queue, s_current, k_m)

        return s_new, k_m


def init_dstarlite(graph, queue, s_start, s_goal, k_m):
    graph.graph[s_goal].rhs = 0
    heapq.heappush(
        queue, 
        calculate_key(graph, s_goal, s_start, k_m) + (s_goal,)
    )
    compute_shortest_path(graph, queue, s_start, k_m)

    return (graph, queue, k_m)
