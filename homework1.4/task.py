
def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'

def calculate():

    #DO NOT USE IMPORT
    #ENTER CODE BELOW HERE
    #ANY CODE ABOVE WILL CAUSE
    #HOMEWORK TO BE GRADED
    #INCORRECT

    p = localize(colors, measurements, motions, sensor_right, p_move)

    #Your probability array must be printed 
    #with the following code.
    show(p)
    return p


def localize(world, measurements, motions, sensor_right, p_move):
    '''
    The function localizes a robot in a 2D world. Assuming that initially the robot has 
    a uniform probability of being in any cell. It also asumes that at each step, the robot:
        1) first makes a movement,
        2) then takes a measurement.

    Returns a 2D list (of the same dimensions as world) that gives the probabilities 
    that the robot occupies each cell in the world.

    world:          a 2D list, each entry either 'R' (red cell) or 'G' (green cell)

    measurements:   a list of measurements taken by the robot, each entry either 'R' or 'G'

    motions:        a list of actions taken by the robot, each entry of the form [dy,dx], where
                    dx refers to the change in the x-direction (positive means right) and
                    dy refers to the change in the y-direction (positive means downward)
                    NOTE: the *first* coordinate is change in y; the *second* coordinate is change in x

    sensor_right:   a float between 0 and 1, giving the probability that any given measurement is
                    correct; the probability that the measurement is incorrect is 1-sensor_right

    p_move:         a float between 0 and 1, giving the probability that any given movement 
                    command takes place; (1-p_move) is the probability that the movement 
                    command fails (and the robot remains still)
    '''
    if len(motions) != len(measurements):
        raise ValueError, "motions and measurements lists should have equal size"

    # initializes p to a uniform distribution over a grid of the same dimensions as world
    pinit = 1.0 / float(len(world)) / float(len(world[0]))
    p = [[pinit for row in range(len(world[0]))] for col in range(len(world))]

    # take one motion and measurement at each step
    for k in range(len(measurements)):
        p = move(p, motions[k], p_move)
        p = sense(p, world, measurements[k], sensor_right)

    return p


def move(p, motion, p_move):
    '''
    Computes the posterior probability after performing motion with p_move probability.

    p:          a priori probability distribution of the location of the robot in the world

    motion:     the action taken by the robot of the form [dy,dx], where dx refers to the change in 
                the x-direction (positive meaning right) and dy refers to the change in the y-direction 
                (positive meaning downward) 
                NOTE: the *first* coordinate is change in y; the *second* coordinate is change in x

    p_move:     a float between 0 and 1, giving the probability that any given movement 
                command takes place; (1-p_move) is the probability that the movement 
                command fails (and the robot remains still)
    '''
    dy,dx = motion
    rows, cols = len(p), len(p[0])

    # create an empty table of the same dimensions of p
    q = [[0.0 for j in range(cols)] for i in range(rows)]

    for row in range(rows):
        for col in range(cols):
            q[row][col] = ((1-p_move)*p[row][col]) + (p_move*p[(row-dy)%rows][(col-dx)%cols])

    return q


def sense(p, world, measurement, sensor_right):
    '''
    Adjust the probability distribution after performing a measurement (sensing the world).
    Locations where the measurement matches the world increase their probability; 
    otherwise probability is decreased.

    p:              a priori probability distribution of the location of the robot in the world

    world:          a 2D list, each entry either 'R' (red cell) or 'G' (green cell)

    measurement:    the measurement taken by the robot, either 'R' or 'G'

    sensor_right:   a float between 0 and 1, giving the probability that the measurement is correct;
                    the probability that the measurement is incorrect is 1-sensor_right

    '''
    rows, cols = len(p), len(p[0])

    # Compute non-normalized posterior probability distribution
    s = 0
    for row in range(rows):
        for col in range(cols):
            hit = (measurement==world[row][col])
            p[row][col] = p[row][col]* ( (hit*sensor_right)+((1-hit)*(1-sensor_right)) )
            # Accumulate normalization parameter
            s += p[row][col]

    # Normalize each value
    for row in range(rows):
        for col in range(cols):
            p[row][col]/=s

    return p

    
#############################################################

if __name__ == '__main__':

    world = [['R','G','G','R','R'],
             ['R','R','G','R','R'],
             ['R','R','G','G','R'],
             ['R','R','R','R','R']]

    measurements = ['G','G','G','G','G']

    motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
    
    p_move = 1
    
    sensor_right = 1

    p = localize(world,measurements,motions,sensor_right,p_move)

    show(p)
