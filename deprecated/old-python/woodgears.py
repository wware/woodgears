from math import pi, sin, cos

# other classes that go up here: LineTo, MoveTo, Path


class Arc(object):
    # http://www.physics.emory.edu/faculty/weeks/graphics/howtops2.html
    def __init__(self, x, y, r, angle1, angle2):
        self.x, self.y, self.r, self.angle1, self.angle2 = x, y, r, angle1, angle2

    def pscmd(self):
        return 'arc'

    def postscript(self, xoffset, yoffset):
        return '{0} {1} {2} {3} {4} {5}'\
            .format(72 * (self.x + xoffset), 72 * (self.y + yoffset), 72 * self.r,
                    self.angle1, self.angle2, self.pscmd())


class Arcn(Arc):
    def pscmd(self):
        return 'arcn'


class Paths(object):

    def __init__(self, *args):
        self._args = args
        self._offset = (0, 0)   # in inches
        self.minx = self.maxx = self.miny = self.maxy = None
        self.paths = []

    def __repr__(self):
        return '<' + self.__class__.__name__ + ' ' + repr(self.paths) + '>'

    def lowerLeftCorner(self):
        self.offset(-self.minx, -self.miny)
        return self

    def addPath(self, path):
        self.paths.append(path)
        self.setMinMax()

    def add(self, other):
        assert isinstance(other, Paths)

        def func(x, y, dx=other._offset[0], dy=other._offset[1]):
            return (x + dx, y + dy)
        for path in other.paths:
            self.addPath(self.transformPath(func, path))

    def read(self, inf):
        currentPath = []
        for x in inf.readlines():
            valid, xy, closePath = self.processInputLine(x.strip())
            if valid:
                if closePath and len(currentPath) > 0:
                    self.paths.append(currentPath)
                    currentPath = []
                self.setMinMax(xy)
                currentPath.append(xy)
        if len(currentPath) > 0:
            self.paths.append(currentPath)

    def centerAtOrigin(self):
        dx, dy = map(lambda x: -x, self.centroid())
        self.translateAllPoints(dx, dy)

    def __add__(self, other):
        assert isinstance(other, Paths)
        other = other.clone()
        other.translateAllPoints(other._offset[0], other._offset[1])
        p = Paths()
        p.paths = self.paths + other.paths
        p._offset = self._offset
        p.minx = min(self.minx, other.minx)
        p.maxx = max(self.maxx, other.maxx)
        p.miny = min(self.miny, other.miny)
        p.maxy = max(self.maxy, other.maxy)
        return p

    def radius(self):
        self.setMinMax()
        xc, yc = self.centroid()
        rad = [0]

        def f(x, y):
            r = ((x - xc)**2 + (y - yc)**2) ** .5
            rad[0] = max(r, rad[0])
        self.forAllPoints(f)
        return rad[0]

    def transformPath(self, func, path):
        def trpt(xy):
            # consider defining a Point class so that Point and Arc
            # can each define their own translate methods
            if isinstance(xy, Arc):
                x, y = func(xy.x, xy.y)
                return xy.__class__(x, y, xy.r, xy.angle1, xy.angle2)
            else:
                x, y = xy
                xy = func(x, y)
                if xy is None:
                    return x, y
                else:
                    return xy
        return map(trpt, path)

    def rotate(self, degrees):
        # clockwise
        radians = (pi / 180) * degrees

        def func(x, y, a=cos(radians), b=-sin(radians), c=sin(radians)):
            # when rotating an Arc, we want to add degrees to angle1 and angle2
            # yet another argument for better polymorphism
            return (a * x + b * y, c * x + a * y)
        return self.forAllPoints(func)

    def forAllPoints(self, func):
        def tr(path):
            return self.transformPath(func, path)
        self.paths = map(tr, self.paths)
        return self

    def translateAllPoints(self, dx, dy):
        self.forAllPoints(lambda x, y: (x + dx, y + dy))
        self.setMinMax()
        return self

    def setMinMax(self, xy=None):
        self.minx = self.maxx = self.miny = self.maxy = None

        def setMinMaxOnePoint(x, y):
            def f(func, m, x):
                return (m is None) and x or func(m, x)
            self.minx = f(min, self.minx, x)
            self.maxx = f(max, self.maxx, x)
            self.miny = f(min, self.miny, y)
            self.maxy = f(max, self.maxy, y)
            return (x, y)
        if xy is None:
            self.forAllPoints(setMinMaxOnePoint)
        else:
            x, y = xy
            setMinMaxOnePoint(x, y)
        return xy

    def clone(self):
        cln = apply(self.__class__, self._args)
        cln.paths = map(lambda path: path[:], self.paths)
        cln.pathprep = self.pathprep
        cln._offset = self._offset
        cln.setMinMax()
        return cln

    def __cmp__(self, other):
        return cmp(self.paths, other.paths)

    def centroid(self):
        return (0.5 * (self.minx + self.maxx), 0.5 * (self.miny + self.maxy))

    def offset(self, dx, dy):
        x, y = self._offset
        self._offset = x + dx, y + dy
        self.setMinMax()
        return self

    def postscript(self, outf=None):
        if outf is None:
            import sys
            outf = sys.stdout
        # don't forget to add header and footer
        pathindex = 0
        xoffset, yoffset = self._offset
        for path in self.paths:
            self.pathprep(outf, pathindex)
            pathindex += 1
            verb = 'moveto'
            for thing in path:
                if isinstance(thing, Arc):
                    outf.write(thing.postscript(xoffset, yoffset) + '\n')
                else:
                    x, y = thing
                    outf.write('{0} {1} {2}\n'.format((x + xoffset) * 72, (y + yoffset) * 72, verb))
                    verb = 'lineto'
            outf.write('stroke\n')

    def pathprep(self, outf, index):
        pass

    def colored(self):
        def pathprep(outf, pathindex):
            colors = [
                (1, 0, 0),    # red
                (1, 0.7, 0),      # orange
                (1, 1, 0),    # yellow
                (0, 1, 0),    # green
                (0, 0, 1),    # blue
                (0.7, 0.3, 1.0)   # purple
            ]
            color = colors[pathindex % len(colors)]
            outf.write(apply('{0} {1} {2} setrgbcolor\n'.format, color))
        self.pathprep = pathprep
        return self


class Circle(Paths):

    def __init__(self, diameter):
        super(Circle, self).__init__(diameter)
        r = 0.5 * diameter
        self.minx = self.miny = -r
        self.maxx = self.maxy = r
        self._diameter = diameter
        self.addPath([
            Arc(0, 0, 0.5 * diameter, 0, 360)
        ])


class Hexagon(Paths):

    @classmethod
    def byHeight(cls, height):
        return cls(height / (3**.5))

    def __init__(self, size):
        super(Hexagon, self).__init__(size)
        hsize = 0.5 * size
        asize = 0.5 * (3**.5) * size
        self.addPath([
            (-size, 0),
            (-hsize, asize),
            (hsize, asize),
            (size, 0),
            (hsize, -asize),
            (-hsize, -asize),
            (-size, 0)
        ])
        self.centerAtOrigin()


class WoodGear(Paths):
    """
    Accepts a HPGL file created by the gear template generator at
    http://woodgears.ca/gear_cutting/template.html. The first path
    will be the bore, the second will be the gear perimeter (the teeth),
    and subsequent paths will be cut-outs for spokes.
    """

    def __init__(self):
        super(WoodGear, self).__init__()
        self._boreRemoved = False

    def read(self, inf):
        if inf is not None:
            self.active = False
            if isinstance(inf, str) or isinstance(inf, unicode):
                inf = open(inf)
            super(WoodGear, self).read(inf)
            self.centerAtOrigin()
        return self

    def clone(self):
        cl = super(WoodGear, self).clone()
        cl._boreRemoved = self._boreRemoved
        return cl

    def removeBore(self):
        if not self._boreRemoved:
            self.paths = self.paths[1:]
            self._boreRemoved = True

    def removeSpokes(self):
        if self._boreRemoved:
            self.paths = self.paths[:1]
        else:
            self.paths = self.paths[:2]

    def processInputLine(self, line):
        def getInches(x):
            return int(x) / (25.4 * 40)
        valid, xy, closePath = False, None, None
        if line == 'SP7;':
            self.active = False
        elif line == 'SP1;':
            self.active = True
        elif self.active and line.startswith('PU '):
            valid = closePath = True
            xy = tuple(map(getInches, line[3:-1].split(',')))
        elif self.active and line.startswith('PD '):
            valid = True
            xy = tuple(map(getInches, line[3:-1].split(',')))
        return valid, xy, closePath


def postscript_page(*gears):
    # goes to stdout
    print '%!PS'
    for gear in gears:
        gear.postscript()
    print 'showpage'
