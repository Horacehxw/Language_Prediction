import numpy as np

def normalize(a, b, c):
    sum = np.sum([a,b,c])
    if sum == 0:
        return a, b, c
    return a / sum, b / sum, c / sum


class Country():
    '''
    The primary unit for simulation of language competitions.

    Only consider 2 or less.

    The outside call of Country should be (update-->transmit*x-->grow)*infty
    '''

    def __init__(self, name_X, name_Y, x, y, b, Ix, Iy, k, Pop, a=1.5, c=0.1):
        '''
        :param X, Y:
            name of each language
        :param x: float in [0,1)
            language X only population fraction
        :param y: float in [0,1)
            language Y only population fraction
        :param b: float in [0,1)
            bilingual population fraction
        :param Ix:
            Influence factor of language X
        :param Iy:
            Influence factor of language Y
        :param k:
            Similarity of X and Y
        :param P:
            Total population of the country
        :param a:
            constant to control the transition probability
        :param c:
            constant to control the evolve speed of dx/dt, dy/dt
        :param Pop: list or array like
            list of the total population on every year
        '''
        self.time = 0
        if name_X == None or name_Y == None:
            if name_X == None:
                name_X, name_Y = name_Y, name_X
                x, y = y, x
                Ix, Iy = Iy, Ix
        elif name_X > name_Y: # maintain the order X <= Y
            x, y = y, x
            name_X, name_Y = name_Y, name_X
            Ix, Iy = Iy, Ix
        self.name_X, self.name_Y, self.k, self.P, self.a, self.c, self.Pop =\
                name_X, name_Y, k, Pop[self.time], a, c, Pop
        self.x, self.y, self.b = normalize(x, y, b)
        self.X, self.Y, self.B = self.x*self.P, self.y*self.P, self.b*self.P
        self.sx = Ix / (Ix + Iy) # sy=1-sx is ignored

    def update(self):
        self.x, self.y, self.b = normalize(self.X, self.Y, self.B)
        dx = self.c * ((1-self.x)*(1-self.k)*self.sx*(1-self.y)**self.a
                       - self.x*(1-self.sx)*(1-self.x)**self.a)

        dy = self.c * ((1-self.y)*(1-self.k)*(1-self.sx)*(1-self.x)**self.a
                       - self.y*self.sx*(1-self.y)**self.a)

        self.x += dx; self.y += dy
        self.b = 1 - self.x - self.y
        self.X, self.Y, self.B = self.x * self.P, self.y * self.P, self.b * self.P

    def transmit(self, other, ratio):
        Xout, Yout, Bout = self.x*self.P*ratio, self.y*self.P*ratio, self.b*self.P*ratio
        self.X -= Xout; self.Y -= Yout; self.B -= Bout
        if self.name_X == other.name_X and self.name_Y == other.name_Y:
            other.X += Xout; other.Y += Yout; other.B += Bout
            remain = 0
        elif self.name_X == other.name_X:
            other.X += Xout + Bout
            remain = Yout
        elif self.name_Y == other.name_Y:
            other.Y += Yout+Bout
            remain = Xout
        elif self.name_X == other.name_Y:
            other.Y += Xout + Bout
            remain = Yout
        elif self.name_Y == other.name_X:
            other.X += Yout + Bout
            remain = Xout
        else:
            remain = Xout + Yout + Bout
        if other.x >= other.y: #the remain immigrants intend to learn the biggest language
            other.X += remain
        else:
            other.Y += remain

    def grow(self):
        '''
        update Population based on the projection data
        '''
        self.time += 1
        P = self.Pop[self.time]
        self.x, self.y, self.b = normalize(self.X, self.Y, self.B)
        self.P = P
        self.X, self.Y, self.B = self.x * P, self.y * P, self.b * P



