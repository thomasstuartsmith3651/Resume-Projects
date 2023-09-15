


class Container():
    '''

    hard coded container with fixed position,velocity and radius

    '''

    def __init__(self,radius=10,position=[0.0,0.0],velocity=[0.0,0.0],mass=10000):
        
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.mass = mass