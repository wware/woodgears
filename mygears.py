#!/usr/bin/env python

from woodgears import *


class Stepper45Degrees(Paths):
	def __init__(self):
		# NEMA 23 stepper with 1/4" axis
		super(Stepper45Degrees, self).__init__()
		self.add(Circle(0.25))
		h = Circle(0.195)
		self.add(h.clone().offset(1.312, 0))
		self.add(h.clone().offset(-1.312, 0))
		self.add(h.clone().offset(0, 1.312))
		self.add(h.offset(0, -1.312))


class MotorHolder(Paths):
	def __init__(self):
		super(MotorHolder, self).__init__()
		self.add(Stepper45Degrees())
		self.add(Circle(0.195).offset(0, 2))
		self.add(Circle(0.195).offset(0, -2))
		self.addPath([
			(0.5, -2.5),
			(0.5, -0.5),
			(2, -0.5),
			(2, 0.5),
			(0.5, 0.5),
			(0.5, 2.5),
			(-0.5, 2.5),
			(-0.5, 0.5),
			(-2, 0.5),
			(-2, -0.5),
			(-2, -0.5),
			(-0.5, -0.5),
			(-0.5, -2.5),
			(0.5, -2.5)
		])


class Slot(Paths):
	def __init__(self, x1, x2, y, r):
		super(Slot, self).__init__(x1, x2, y, r)
		if x2 < x1:
			x1, x2 = x2, x1
		self.addPath([
			Arc(x1, y, r, 90, 270),
			(x1, y - r),
			(x2, y - r),
			Arc(x2, y, r, 270, 450),
			(x2, y + r),
			(x1, y + r)
		])


class GearPlate(Paths):
	def __init__(self):
		super(GearPlate, self).__init__()
		self.add(Circle(0.195).offset(-2.5, 3))
		self.add(Circle(0.195).offset(2, 3))
		self.add(Circle(0.195).offset(-2.5, -3))
		self.add(Circle(0.195).offset(2, -3))
		self.add(Circle(0.250).offset(0, 1.5))
		self.add(Circle(0.250).offset(0, -1.5))
		self.add(Slot(-2.5, -1.5, 2, 0.097))
		self.add(Slot(-2.5, -1.5, -2, 0.097))
		self.addPath([
			(-3, -3.5),
			(2.5, -3.5),
			(2.5, 3.5),
			(-3, 3.5),
			(-3, 1.5),
			(-0.5, 1.5),
			Arc(0, 1.5, 0.5, 180, 360),
			(1, 1.5),
			(1, -1.5),
			Arc(0, -1.5, 0.5, 0, 180),
			(-0.5, -1.5),
			(-3, -1.5),
			(-3, -3.5)
		])


class MotorGear(WoodGear):
	def __init__(self):
		super(MotorGear, self).__init__()
		self.read('gear.plt')
		self.centerAtOrigin()


class NutGear(MotorGear):
	def __init__(self):
		super(NutGear, self).__init__()
		self.removeBore()   # replace the bore hole with a hex cut-out for the nut
		# According to http://www.fastenal.com/web/products/details/0147964,
		# a 1/4-20 nut has a wrench size of 7/16".
		self.add(Hexagon.byHeight(7./16))



g1 = MotorGear()
g2 = NutGear()
g3 = NutGear()

r = g1.radius()
g1.offset(0.5 + r, 0.5 + r)
g2.offset(0.5 + r, 0.5 + 3 * r)
g3.offset(0.5 + r, 0.5 + 5 * r)

stepper45degrees = MotorHolder().offset(5.5, 3)

postscript_page(g1, g2, g3, stepper45degrees)

gp = GearPlate().lowerLeftCorner().offset(0.5, 0.5)
postscript_page(gp)
# gp2 = GearPlate().lowerLeftCorner().rotate(45).offset(0.5, 0.5)
# postscript_page(gp, gp2)
