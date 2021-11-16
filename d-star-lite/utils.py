

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

def add_reroute_obstacle(graph, s_current, s_next):
    '''
        Add a redirect obstacle by blocking the next spot
        works specifically for maps of this type
        W W W W W W W W W W W W 
        W                     W 
        W   R X               W 
        W   X X               W 
        W                     W 
        W                     W 
        W                     W 
        W                     W 
        W               X X   W 
        W               X G   W 
        W                     W 
        W W W W W W W W W W W W 
    
    '''
    #TODO: Fix the redirect
    success = False

    if s_next != 'goal':
        # print(f's_new={s_next}')
        col, row = stateNameToCoords(s_next)
        
        if(graph.cells[row + 1][col] == 0):
            graph.cells[row + 1][col] = -1
            success = True

        # true if obstacle was added, false if
        #  no obstacles could have been added
    return success 
    