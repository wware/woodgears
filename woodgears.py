class Paths(object):
	def __init__(self):
		self._offset = (0, 0)   # in inches
		self.minx = self.maxx = self.miny = self.maxy = None
		self.paths = []

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
		assert self._offset == other._offset
		p = Paths()
		p.paths = self.paths + other.paths
		p._offset = self._offset
		p.minx = min(self.minx, other.minx)
		p.maxx = max(self.maxx, other.maxx)
		p.miny = min(self.miny, other.miny)
		p.maxy = max(self.maxy, other.maxy)
		return p

	def radius(self):
		xc, yc = self.centroid()
		rad = [0]
		def f(x, y):
			r = ((x - xc)**2 + (y - yc)**2) ** .5
			rad[0] = max(r, rad[0])
		self.forAllPoints(f)
		return rad[0]

	def forAllPoints(self, func):
		def tr(path):
			def trpt(xy):
				x, y = xy
				xy = func(x, y)
				if xy is None:
					return x, y
				else:
					return xy
			return map(trpt, path)
		self.paths = map(tr, self.paths)

	def translateAllPoints(self, dx, dy):
		self.forAllPoints(lambda x, y: (x + dx, y + dy))
		self.minx, self.maxx = self.minx + dx, self.maxx + dx
		self.miny, self.maxy = self.miny + dy, self.maxy + dy

	def setMinMax(self, xy=None):
		def setMinMaxOnePoint(x, y):
			def f(func, m, x):
				return (m is None) and x or func(m, x)
			self.minx = f(min, self.minx, x)
			self.maxx = f(max, self.maxx, x)
			self.miny = f(min, self.miny, y)
			self.maxy = f(max, self.maxy, y)
		if xy is None:
			self.forAllPoints(setMinMaxOnePoint)
		else:
			x, y = xy
			setMinMaxOnePoint(x, y)

	def clone(self):
		cln = self.__class__()
		cln.paths = map(lambda path: path[:], self.paths)
		cln.pathprep = self.pathprep
		cln._offset = self._offset
		return cln

	def __cmp__(self, other):
		return cmp(self.paths, other.paths)

	def centroid(self):
		return (0.5 * (self.minx + self.maxx), 0.5 * (self.miny + self.maxy))

	def offset(self, dx, dy):
		x, y = self._offset
		self._offset = x + dx, y + dy

	def postscript(self, outf):
		# don't forget to add header and footer
		pathindex = 0
		xoffset, yoffset = self._offset
		for path in self.paths:
			self.pathprep(outf, pathindex)
			pathindex += 1
			verb = 'moveto'
			for x, y in path:
				outf.write('{0} {1} {2}\n'.format((x + xoffset) * 72, (y + yoffset) * 72, verb))
				verb = 'lineto'
			outf.write('stroke\n')

	def pathprep(self, outf, index):
		pass

	def colored(self):
		def pathprep(outf, pathindex):
			colors = [
				(1, 0, 0),        # red
				(1, 0.7, 0),      # orange
				(1, 1, 0),        # yellow
				(0, 1, 0),        # green
				(0, 0, 1),        # blue
				(0.7, 0.3, 1.0)   # purple
			]
			color = colors[pathindex % len(colors)]
			outf.write(apply('{0} {1} {2} setrgbcolor\n'.format, color))
		self.pathprep = pathprep


class Hexagon(Paths):

	@classmethod
	def byHeight(cls, height):
		return cls(height / (3**.5))

	def __init__(self, size):
		super(Hexagon, self).__init__()
		a = 0.5 * (3**.5)
		self.paths = [
			[
				(-size, 0),
				(-0.5 * size, a * size),
				(0.5 * size, a * size),
				(size, 0),
				(0.5 * size, -a * size),
				(-0.5 * size, -a * size),
				(-size, 0)
			]
		]


class WoodGear(Paths):
	"""
	Accepts a HPGL file created by the gear template generator at
	http://woodgears.ca/gear_cutting/template.html. The first path
	will be the bore, the second will be the gear perimeter (the teeth),
	and subsequent paths will be cut-outs for spokes.
	"""

	def __init__(self, inf=None):
		super(WoodGear, self).__init__()
		self._boreRemoved = False
		if inf is not None:
			self.active = False
			if isinstance(inf, str) or isinstance(inf, unicode):
				inf = open(inf)
			self.read(inf)
			self.centerAtOrigin()

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
	import sys
	print '%!PS'
	for gear in gears:
		gear.postscript(sys.stdout)
	print 'showpage'