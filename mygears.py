#!/usr/bin/env python

from woodgears import *

g1 = WoodGear('gear.plt')
# According to http://www.fastenal.com/web/products/details/0147964,
# a 1/4-20 nut has a wrench size of 7/16".
g2 = g1.clone()
g2.removeBore()   # replace the bore hole with a hex cut-out for the nut
g2 += Hexagon.byHeight(7./16)
g3 = g2.clone()

r = g1.radius()
g1.offset(0.5 + r, 0.5 + r)
g2.offset(0.5 + r, 0.5 + 3 * r)
g3.offset(0.5 + r, 0.5 + 5 * r)
postscript_page(g1, g2, g3)