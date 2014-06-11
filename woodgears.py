#!/usr/bin/env python
# Usage: python woodgears.py < gear.plt > gear.ps

import sys

printing = False
drawn = False

print '%!PS'

def transform_xy(x, y):
	SCALE = 72./(25.4 * 40)
	return (SCALE * x + 36, SCALE * y + 36)

for x in sys.stdin.readlines():
	x = x.strip()
	if x == 'SP7;':
		printing = False
	elif x == 'SP1;':
		printing = True
	elif printing:
		if x.startswith('PU '):
			if drawn:
				print 'stroke'
			x, y = map(int, x[3:-1].split(','))
			print apply('{0} {1} moveto'.format, transform_xy(x, y))
		elif x.startswith('PD '):
			drawn = True
			x, y = map(int, x[3:-1].split(','))
			print apply('{0} {1} lineto'.format, transform_xy(x, y))

print 'stroke'
print 'showpage'
