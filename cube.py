"""Generalized Rubik's Cube."""
import re
from random import randint

class Cube(object):
    FACES = (FRONT, BACK, LEFT, RIGHT, UP, DOWN) = ('f','b','l','r','u','d')
    COLORS = {
        'b': u'\u001b[38;5;33mb\u001b[0m',
        'r': u'\u001b[38;5;9mr\u001b[0m',
        'g': u'\u001b[38;5;10mg\u001b[0m',
        'o': u'\u001b[38;5;208mo\u001b[0m',
        'y': u'\u001b[38;5;11my\u001b[0m',
    }
    TURN = re.compile(r"(\d*)([fblrud])('?)(\d*)", re.I)
    ROTATION = re.compile(r"([xyz])('?)(\d*)", re.I)
    ACTION = re.compile(r"(?:\d*[fblrud]'?\d*)|(?:[xyz]'?\d*)", re.I)
    
    def __init__(self, size, f='w', b='y', l='b', r='g', u='r', d='o'):
        self.size = size
        self.colors = (f, b , l , r , u, d)
        self.cube = dict(zip(
            Cube.FACES,
            [[(color,)*size]*size for color in self.colors],
        ))

    def __str__(self):
        format_row = lambda x: '[{}]'.format(' '.join(x))
        rshift_row = lambda x: x.rjust(2*len(x))
        
        high = self.cube[Cube.UP]
        high = map(format_row, high)
        high = map(rshift_row, high)
        high = '\n'.join(high)
        
        mid = zip(
            self.cube[Cube.LEFT],
            self.cube[Cube.FRONT],
            self.cube[Cube.RIGHT],
            self.cube[Cube.BACK],
        )
        mid = map(lambda x: map(format_row, x), mid)
        mid = map(''.join, mid)
        mid = '\n'.join(mid)
        
        low = self.cube[Cube.DOWN]
        low = map(format_row, low)
        low = map(rshift_row, low)
        low = '\n'.join(low)
        
        cube = '\n'.join([high, mid, low])
        for color in self.colors:
            if color in Cube.COLORS:
                cube = cube.replace(color, Cube.COLORS[color])
        return cube

    def x(self, cc=False):
        f = self.cube[Cube.FRONT]
        u = self.cube[Cube.UP]
        b = self.cube[Cube.BACK]
        d = self.cube[Cube.DOWN]
        if cc:
            self.cube[Cube.RIGHT] = list(reversed(zip(*self.cube[Cube.RIGHT])))
            self.cube[Cube.LEFT] = zip(*reversed(self.cube[Cube.LEFT]))
            self.cube[Cube.FRONT] = u
            self.cube[Cube.UP] = [row[::-1] for row in reversed(b)]
            self.cube[Cube.BACK] = [row[::-1] for row in reversed(d)]
            self.cube[Cube.DOWN] = f
        else:
            self.cube[Cube.RIGHT] = zip(*reversed(self.cube[Cube.RIGHT]))
            self.cube[Cube.LEFT] = list(reversed(zip(*self.cube[Cube.LEFT])))
            self.cube[Cube.FRONT] = d
            self.cube[Cube.UP] = f
            self.cube[Cube.BACK] = [row[::-1] for row in reversed(u)]
            self.cube[Cube.DOWN] = [row[::-1] for row in reversed(b)]

    def y(self, cc=False):
        l = self.cube[Cube.LEFT]
        b = self.cube[Cube.BACK]
        r = self.cube[Cube.RIGHT]
        f = self.cube[Cube.FRONT]
        if cc:
            self.cube[Cube.UP] = list(reversed(zip(*self.cube[Cube.UP])))
            self.cube[Cube.DOWN] = zip(*reversed(self.cube[Cube.DOWN]))
            self.cube[Cube.LEFT] = b
            self.cube[Cube.BACK] = r
            self.cube[Cube.RIGHT] = f
            self.cube[Cube.FRONT] = l
        else:
            self.cube[Cube.UP] = zip(*reversed(self.cube[Cube.UP]))
            self.cube[Cube.DOWN] = list(reversed(zip(*self.cube[Cube.DOWN])))
            self.cube[Cube.LEFT] = f
            self.cube[Cube.BACK] = l
            self.cube[Cube.RIGHT] = b
            self.cube[Cube.FRONT] = r

    def z(self, cc=False):
        l = self.cube[Cube.LEFT]
        u = self.cube[Cube.UP]
        r = self.cube[Cube.RIGHT]
        d = self.cube[Cube.DOWN]
        if cc:
            self.cube[Cube.FRONT] = list(reversed(zip(*self.cube[Cube.FRONT])))
            self.cube[Cube.BACK] = zip(*reversed(self.cube[Cube.BACK]))
            self.cube[Cube.LEFT] = list(reversed(zip(*u)))
            self.cube[Cube.UP] = list(reversed(zip(*r)))
            self.cube[Cube.RIGHT] = list(reversed(zip(*d)))
            self.cube[Cube.DOWN] = list(reversed(zip(*l)))
        else:
            self.cube[Cube.FRONT] = zip(*reversed(self.cube[Cube.FRONT]))
            self.cube[Cube.BACK] = list(reversed(zip(*self.cube[Cube.BACK])))
            self.cube[Cube.LEFT] = zip(*reversed(d))
            self.cube[Cube.UP] = zip(*reversed(l))
            self.cube[Cube.RIGHT] = zip(*reversed(u))
            self.cube[Cube.DOWN] = zip(*reversed(r))

    def rotate(self, axis, cc=False):
        getattr(self, axis.lower())(cc)
    
    def f(self, cc=False, layers=1):
        if not (0 < layers <= self.size):
            return
        if layers == self.size:
            return self.z(cc)
        self.x()
        self.u(cc, layers)
        self.x(True)
    
    def b(self, cc=False, layers=1):
        if not (0 < layers <= self.size):
            return
        if layers == self.size:
            return self.z(not cc)
        self.x(True)
        self.u(cc, layers)
        self.x()
    
    def l(self, cc=False, layers=1):
        if not (0 < layers <= self.size):
            return
        if layers == self.size:
            return self.x(not cc)
        self.z()
        self.u(cc, layers)
        self.z(True)
    
    def r(self, cc=False, layers=1):
        if not (0 < layers <= self.size):
            return
        if layers == self.size:
            return self.x(cc)
        self.z(True)
        self.u(cc, layers)
        self.z()
    
    def u(self, cc=False, layers=1):
        if not (0 < layers <= self.size):
            return
        if layers == self.size:
            return self.y(cc)
        l = self.cube[Cube.LEFT][:layers]
        b = self.cube[Cube.BACK][:layers]
        r = self.cube[Cube.RIGHT][:layers]
        f = self.cube[Cube.FRONT][:layers]
        if cc:
            self.cube[Cube.UP] = list(reversed(zip(*self.cube[Cube.UP])))
            self.cube[Cube.LEFT][:layers] = b
            self.cube[Cube.BACK][:layers] = r
            self.cube[Cube.RIGHT][:layers] = f
            self.cube[Cube.FRONT][:layers] = l
        else:
            self.cube[Cube.UP] = zip(*reversed(self.cube[Cube.UP]))
            self.cube[Cube.LEFT][:layers] = f
            self.cube[Cube.BACK][:layers] = l
            self.cube[Cube.RIGHT][:layers] = b
            self.cube[Cube.FRONT][:layers] = r
    
    def d(self, cc=False, layers=1):
        if not (0 < layers <= self.size):
            return
        if layers == self.size:
            return self.y(not cc)
        l = self.cube[Cube.LEFT][-layers:]
        f = self.cube[Cube.FRONT][-layers:]
        r = self.cube[Cube.RIGHT][-layers:]
        b = self.cube[Cube.BACK][-layers:]
        if cc:
            self.cube[Cube.DOWN] = list(reversed(zip(*self.cube[Cube.DOWN])))
            self.cube[Cube.LEFT][-layers:] = f
            self.cube[Cube.FRONT][-layers:] = r
            self.cube[Cube.RIGHT][-layers:] = b
            self.cube[Cube.BACK][-layers:] = l
        else:
            self.cube[Cube.DOWN] = zip(*reversed(self.cube[Cube.DOWN]))
            self.cube[Cube.LEFT][-layers:] = b
            self.cube[Cube.FRONT][-layers:] = l
            self.cube[Cube.RIGHT][-layers:] = f
            self.cube[Cube.BACK][-layers:] = r

    def turn(self, face, cc=False, layers=1):
        getattr(self, face.lower())(cc, layers)

    def do(self, action):
        turn = Cube.TURN.match(action)
        if turn:
            layers, face, cc, times = turn.groups()
            layers = int(layers) if layers else 1
            times = (int(times) if times else 1) % 4
            for time in xrange(times):
                self.turn(face, cc, layers)
        else:
            rotation = Cube.ROTATION.match(action)
            if rotation:
                axis, cc, times = rotation.groups()
                times = (int(times) if times else 1) % 4
                for time in xrange(times):
                    self.rotate(axis, cc)

    def run(self, algorithm):
        map(self.do, Cube.ACTION.findall(algorithm))
        
    def scramble(self):
        faces = self.cube.keys()
        for i in xrange(12*self.size):
            self.turn(faces[randint(0,5)], randint(0,1), randint(1,self.size))
