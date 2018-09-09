from random import choice, randrange
from re import compile, I


class Cube(object):
    """Generalized Rubik's Cube.

    This implementation assumes that you are familiar with large Rubik's Cube notation.
    Examples:
        l - turn the left face clockwise (as if you were looking at it) once (i.e. 90 degrees)
        u' - turn the up (aka top) face counterclockwise once
        r2 - turn the right face clockwise twice (i.e. 180 degrees)
        2f - turn the first two layers on the front side clockwise
        2B - turn the second layer in from the back side clockwise
        3D'2 - turn the third layer in from the down (aka bottom) side counterclockwise twice
        l u' r2 2f 2B 3D'2 - perform the actions mentioned above in sequence
    Check out http://w.astro.berkeley.edu/~converse/rubiks.php?id1=basics&id2=largenotation for a more detailed explanation.

    Run in terminal with dark background to see colors.
    """

    FACES = (FRONT, BACK, LEFT, RIGHT, UP, DOWN) = 'fblrud'
    # ansi escape color codes
    COLORS = {
        'b': u'\u001b[38;5;33mb\u001b[0m',
        'r': u'\u001b[38;5;9mr\u001b[0m',
        'g': u'\u001b[38;5;10mg\u001b[0m',
        'o': u'\u001b[38;5;208mo\u001b[0m',
        'y': u'\u001b[38;5;11my\u001b[0m',
    }
    # Rubik's Cube notation definitions
    TURN = compile(r"(\d*)([fblrud])('?)(\d*)", I)
    ROTATION = compile(r"([xyz])('?)(\d*)", I)
    ACTION = compile(r"(?:\d*[fblrud]'?\d*)|(?:[xyz]'?\d*)", I)
    
    def __init__(self, size, f='w', b='y', l='b', r='g', u='r', d='o'):
        self.size = size
        self.colors = (f, b , l , r , u, d)
        # one matrix of "stickers" for each face
        self.cube = dict(zip(Cube.FACES, [[(color,)*size]*size for color in self.colors]))

    def __str__(self):
        """Get a net of the cube."""
        def format_row(row):
            return '[{}]'.format(' '.join(row))
        def rshift_row(row):
            return row.rjust(2*len(row))
        
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
        mid = [map(format_row, row) for row in mid]
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

    @classmethod
    def _rotate_matrix(cls, matrix, counterclockwise=False):
        return list(reversed(zip(*matrix))) if counterclockwise else zip(*reversed(matrix))

    @classmethod
    def _reverse_matrix(cls, matrix):
        return [row[::-1] for row in reversed(matrix)]

    def x(self, counterclockwise=False):
        """Rotation about the x-axis."""
        f = self.cube[Cube.FRONT]
        u = self.cube[Cube.UP]
        b = self.cube[Cube.BACK]
        d = self.cube[Cube.DOWN]
        if counterclockwise:
            self.cube[Cube.RIGHT] = self._rotate_matrix(self.cube[Cube.RIGHT], True)
            self.cube[Cube.LEFT] = self._rotate_matrix(self.cube[Cube.LEFT])
            self.cube[Cube.FRONT] = u
            self.cube[Cube.UP] = self._reverse_matrix(b)
            self.cube[Cube.BACK] = self._reverse_matrix(d)
            self.cube[Cube.DOWN] = f
        else:
            self.cube[Cube.RIGHT] = self._rotate_matrix(self.cube[Cube.RIGHT])
            self.cube[Cube.LEFT] = self._rotate_matrix(self.cube[Cube.LEFT], True)
            self.cube[Cube.FRONT] = d
            self.cube[Cube.UP] = f
            self.cube[Cube.BACK] = self._reverse_matrix(u)
            self.cube[Cube.DOWN] = self._reverse_matrix(b)

    def y(self, counterclockwise=False):
        """Rotation about the y-axis."""
        l = self.cube[Cube.LEFT]
        b = self.cube[Cube.BACK]
        r = self.cube[Cube.RIGHT]
        f = self.cube[Cube.FRONT]
        if counterclockwise:
            self.cube[Cube.UP] = self._rotate_matrix(self.cube[Cube.UP], True)
            self.cube[Cube.DOWN] = self._rotate_matrix(self.cube[Cube.DOWN])
            self.cube[Cube.LEFT] = b
            self.cube[Cube.BACK] = r
            self.cube[Cube.RIGHT] = f
            self.cube[Cube.FRONT] = l
        else:
            self.cube[Cube.UP] = self._rotate_matrix(self.cube[Cube.UP])
            self.cube[Cube.DOWN] = self._rotate_matrix(self.cube[Cube.DOWN], True)
            self.cube[Cube.LEFT] = f
            self.cube[Cube.BACK] = l
            self.cube[Cube.RIGHT] = b
            self.cube[Cube.FRONT] = r

    def z(self, counterclockwise=False):
        """Rotation about the z-axis."""
        l = self.cube[Cube.LEFT]
        u = self.cube[Cube.UP]
        r = self.cube[Cube.RIGHT]
        d = self.cube[Cube.DOWN]
        if counterclockwise:
            self.cube[Cube.FRONT] = self._rotate_matrix(self.cube[Cube.FRONT], True)
            self.cube[Cube.BACK] = self._rotate_matrix(self.cube[Cube.BACK])
            self.cube[Cube.LEFT] = self._rotate_matrix(u, True)
            self.cube[Cube.UP] = self._rotate_matrix(r, True)
            self.cube[Cube.RIGHT] = self._rotate_matrix(d, True)
            self.cube[Cube.DOWN] = self._rotate_matrix(l, True)
        else:
            self.cube[Cube.FRONT] = self._rotate_matrix(self.cube[Cube.FRONT])
            self.cube[Cube.BACK] = self._rotate_matrix(self.cube[Cube.BACK], True)
            self.cube[Cube.LEFT] = self._rotate_matrix(d)
            self.cube[Cube.UP] = self._rotate_matrix(l)
            self.cube[Cube.RIGHT] = self._rotate_matrix(u)
            self.cube[Cube.DOWN] = self._rotate_matrix(r)

    def rotate(self, axis, counterclockwise=False):
        """Rotation about the given axis."""
        getattr(self, axis.lower())(counterclockwise)
    
    def f(self, counterclockwise=False, layers=1):
        """Turn the front face 90 degrees."""
        if 0 < layers <= self.size:
            if layers == self.size:
                return self.z(counterclockwise)
            self.x()
            self.u(counterclockwise, layers)
            self.x(True)
    
    def b(self, counterclockwise=False, layers=1):
        """Turn the back face 90 degrees."""
        if 0 < layers <= self.size:
            if layers == self.size:
                return self.z(not counterclockwise)
            self.x(True)
            self.u(counterclockwise, layers)
            self.x()
    
    def l(self, counterclockwise=False, layers=1):
        """Turn the left face 90 degrees."""
        if 0 < layers <= self.size:
            if layers == self.size:
                return self.x(not counterclockwise)
            self.z()
            self.u(counterclockwise, layers)
            self.z(True)
    
    def r(self, counterclockwise=False, layers=1):
        """Turn the right face 90 degrees."""
        if 0 < layers <= self.size:
            if layers == self.size:
                return self.x(counterclockwise)
            self.z(True)
            self.u(counterclockwise, layers)
            self.z()
    
    def u(self, counterclockwise=False, layers=1):
        """Turn the up face 90 degrees."""
        if 0 < layers <= self.size:
            if layers == self.size:
                return self.y(counterclockwise)
            l = self.cube[Cube.LEFT][:layers]
            b = self.cube[Cube.BACK][:layers]
            r = self.cube[Cube.RIGHT][:layers]
            f = self.cube[Cube.FRONT][:layers]
            if counterclockwise:
                self.cube[Cube.UP] = self._rotate_matrix(self.cube[Cube.UP], True)
                self.cube[Cube.LEFT][:layers] = b
                self.cube[Cube.BACK][:layers] = r
                self.cube[Cube.RIGHT][:layers] = f
                self.cube[Cube.FRONT][:layers] = l
            else:
                self.cube[Cube.UP] = self._rotate_matrix(self.cube[Cube.UP])
                self.cube[Cube.LEFT][:layers] = f
                self.cube[Cube.BACK][:layers] = l
                self.cube[Cube.RIGHT][:layers] = b
                self.cube[Cube.FRONT][:layers] = r
    
    def d(self, counterclockwise=False, layers=1):
        """Turn the down face 90 degrees."""
        if 0 < layers <= self.size:
            if layers == self.size:
                return self.y(not counterclockwise)
            l = self.cube[Cube.LEFT][-layers:]
            f = self.cube[Cube.FRONT][-layers:]
            r = self.cube[Cube.RIGHT][-layers:]
            b = self.cube[Cube.BACK][-layers:]
            if counterclockwise:
                self.cube[Cube.DOWN] = self._rotate_matrix(self.cube[Cube.DOWN], True)
                self.cube[Cube.LEFT][-layers:] = f
                self.cube[Cube.FRONT][-layers:] = r
                self.cube[Cube.RIGHT][-layers:] = b
                self.cube[Cube.BACK][-layers:] = l
            else:
                self.cube[Cube.DOWN] = self._rotate_matrix(self.cube[Cube.DOWN])
                self.cube[Cube.LEFT][-layers:] = b
                self.cube[Cube.FRONT][-layers:] = l
                self.cube[Cube.RIGHT][-layers:] = f
                self.cube[Cube.BACK][-layers:] = r

    def turn(self, face, counterclockwise=False, layers=1):
        """Turn the given face 90 degrees."""
        getattr(self, face.lower())(counterclockwise, layers)
        if face != face.lower():
            getattr(self, face.lower())(not counterclockwise, layers - 1)

    def do(self, action):
        """Perform the given action on the cube."""
        turn = Cube.TURN.match(action)
        if turn:
            layers, face, counterclockwise, times = turn.groups()
            layers = int(layers) if layers else 1
            times = (int(times) if times else 1) % 4
            for time in xrange(times):
                self.turn(face, counterclockwise, layers)
        else:
            rotation = Cube.ROTATION.match(action)
            if rotation:
                axis, counterclockwise, times = rotation.groups()
                times = (int(times) if times else 1) % 4
                for time in xrange(times):
                    self.rotate(axis, counterclockwise)

    def run(self, algorithm):
        """Perform a series of actions on the cube."""
        map(self.do, Cube.ACTION.findall(algorithm))
        
    def scramble(self):
        """Perform a series of random actions on the cube."""
        faces = self.cube.keys()
        for i in xrange(len(faces)*2*self.size):
            self.turn(choice(faces), randrange(2), 1 + randrange(self.size))

    def is_solved(self):
        """Check whether or not the cube is solved."""
        for face in self.cube.values():
            if len(reduce(lambda x, y: x | y, map(set, face))) != 1:
                return False
        return True

    def play(self):
        """Can you solve it?"""
        while not self.is_solved():
            print self
            self.run(raw_input('Next move? '))
        print self
        print "You're a genius! You solved it!!!"


if __name__ == '__main__':
    c = Cube(3)
    c.scramble()
    c.play()
