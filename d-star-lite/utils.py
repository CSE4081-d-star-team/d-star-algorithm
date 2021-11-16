

def stateNameToCoords(name):
    '''                   x  y
        from x1y2 return [1, 2]
        from x5y4 return [5, 4]
    '''
    row = int(name.split('x')[1].split('y')[0])
    col = int(name.split('x')[1].split('y')[1])
    return (row, col)

def parseDims(filepath):
    '''
        read the dimension of the grid
    '''
    x_dim, y_dim = 0, 0 
    with open(filepath) as F:
        for line in F:
            x_dim += 1
            y_dim = len(line) // 2

    x_dim -= 2
    y_dim -= 2
    
    print(x_dim, y_dim)
    return x_dim, y_dim

def add_reroute_obstacle(graph, s_next):
    '''Add a redirect obstacle by blocking the next spot'''
    
    success = False

    if s_next != 'goal':
        print(f's_new={s_next}')
        row, col = stateNameToCoords(s_next)
        if(graph.cells[row][col] == 0):
            graph.cells[row][col] = -1
            success = True

        # true if obstacle was added, false if
        #  no obstacles could have been added
    return success 
    