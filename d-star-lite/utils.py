

def stateNameToCoords(name):
    '''                   x  y
        from x1y2 return [1, 2]
        from x5y4 return [5, 4]
    '''
    return [
        int(name.split('x')[1].split('y')[0]), 
        int(name.split('x')[1].split('y')[1])
    ]

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

def add_obstacles(gridsize, ):
    '''Return a list of obstacles to redirect the graph'''
    return 