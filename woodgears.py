#!/usr/bin/env python
# Usage: python woodgears.py < gear.plt > gear.ps

import sys
import StringIO


def postscript_page(*gears):
	print '%!PS'
	for gear in gears:
		gear.postscript(sys.stdout)
	print 'showpage'


class Gear:

	def __init__(self, inf):
		self.offset = (0, 0)   # in inches
		self.minx = self.maxx = self.miny = self.maxy = None
		self.paths = []
		currentPath = []
		def getInches(x):
			return int(x) / (25.4 * 40)
		active = False
		for x in inf.readlines():
			x = x.strip()
			if x == 'SP7;':
				active = False
			elif x == 'SP1;':
				active = True
			elif active:
				if x.startswith('PU '):
					if currentPath:
						self.paths.append(currentPath)
						currentPath = []
					xy = tuple(map(getInches, x[3:-1].split(',')))
					self.setMinMax(xy)
					currentPath.append(xy)
				elif x.startswith('PD '):
					xy = tuple(map(getInches, x[3:-1].split(',')))
					self.setMinMax(xy)
					currentPath.append(xy)
		self.paths.append(currentPath)

	def setMinMax(self, xy):
		def f(func, m, x):
			return (m is None) and x or func(m, x)
		self.minx = f(min, self.minx, xy[0])
		self.maxx = f(max, self.maxx, xy[0])
		self.miny = f(min, self.miny, xy[1])
		self.maxy = f(max, self.maxy, xy[1])

	def clone(self):
		f = StringIO.StringIO()
		g = Gear(f)
		g.paths = map(lambda path: path[:], self.paths)
		return g

	def __cmp__(self, other):
		return cmp(self.paths, other.paths)

	def centroid(self):
		return (0.5 * (self.minx + self.maxx), 0.5 * (self.miny + self.maxy))

	def postscript(self, outf):
		# don't forget to add header and footer
		pathindex = 0
		xoffset, yoffset = self.offset
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
			colors = {
				'red': (1, 0, 0),
				'orange': (1, 0.7, 0),
				'yellow': (1, 1, 0),
				'green': (0, 1, 0),
				'blue': (0, 0, 1),
				'purple': (0.7, 0.3, 1.0)
			}
			colorname = 'red,orange,yellow,green,blue,purple'.split(',')[pathindex]
			outf.write(apply('{0} {1} {2} setrgbcolor\n'.format, colors[colorname]))
		self.pathprep = pathprep


g = Gear(open('gear.plt'))
if True:
	gcl = g.clone()
	# gcl.paths.pop(0)
	assert g == gcl
	print g.centroid()
	raise SystemExit
# g.colored()    # the bore is the first (red) path
g.offset = (0.5, 0.5)
postscript_page(g)