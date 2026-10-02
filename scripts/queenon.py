'''funcion que tome las cordenadas discretas de la matriz y mape un plano continuo'''
def get_coordinates(board,row,col):
    # Get the size of the board
    n = len(board)
    
    # Calculate the x and y coordinates based on the row and column
    x=(col/(n-1))-0.5
    y=(row/(n-1))-0.5
    board[row][col] = (x,y)
    return (x,y)
  
def entropy_concave(board): 
    #calculate center zone with euclidian distance between all queens
    center = (0,0)
    coordinates = []
    raw_weigh=[]
    n = len(board)
    for row in range(n-1):
        for col in range(n-1):
            x,y = get_coordinates(board,row,col)
            coordinates.append((x,y))
            #calculate distance to center and weight
            raw_weigh.append((x**2+y**2)**2)
    
    sum_weights = sum(raw_weigh)
    #normalize weights
    probabilities = [w/sum_weights for w in raw_weigh]
    return coordinates, probabilities

