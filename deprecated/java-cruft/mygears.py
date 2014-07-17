import sys
sys.path.append("target/Parts-0.0.1-SNAPSHOT.jar")
from net.willware.parts import *   # NOQA
from stepper import StepperNEMA23


class Rectangle(Part):
    def __init__(self, width, height):
        self.add(Path([
            MoveTo(0, 0),
            LineTo(0, height),
            LineTo(width, height),
            LineTo(width, 0),
            LineTo(0, 0)
        ]))


class RectangleMinusCorner(Part):
    def __init__(self, width, height):
        self.add(Path([
            MoveTo(0, 0),
            LineTo(0, height),
            LineTo(0.5 * width, height),
            LineTo(width, 0.5 * height),
            LineTo(width, 0),
            LineTo(0, 0)
        ]))


class GearPlate(Part):
    def __init__(self):
        self.addHole(-2.5, 3, 0.195)
        self.addHole(2, 3, 0.195)
        self.addHole(-2.5, -3, 0.195)
        self.addHole(2, -3, 0.195)
        self.addHole(0, 1.5, 0.250)
        self.addHole(0, -1.5, 0.250)
        self.add(HorizontalSlot(-2.5, -1.5, 2, 0.195))
        self.add(HorizontalSlot(-2.5, -1.5, -2, 0.195))
        self.add(Path([
            MoveTo(-3, -3.5),
            LineTo(2.5, -3.5),
            LineTo(2.5, 3.5),
            LineTo(-3, 3.5),
            LineTo(-3, 1.5),
            LineTo(-0.5, 1.5),
            Arc(0, 1.5, 0.5, 180, 360),
            LineTo(1, 1.5),
            LineTo(1, -1.5),
            Arc(0, -1.5, 0.5, 0, 180),
            LineTo(-0.5, -1.5),
            LineTo(-3, -1.5),
            LineTo(-3, -3.5)
        ]))


class MotorPlate(Part):
    def __init__(self):
        self.add(StepperNEMA23().rotate(45).centerAtOrigin())
        self.add(Path([
            MoveTo(0.5, -2.5),
            LineTo(0.5, -0.5),
            LineTo(2, -0.5),
            LineTo(2, 0.5),
            LineTo(0.5, 0.5),
            LineTo(0.5, 2.5),
            LineTo(-0.5, 2.5),
            LineTo(-0.5, 0.5),
            LineTo(-2, 0.5),
            LineTo(-2, -0.5),
            LineTo(-2, -0.5),
            LineTo(-0.5, -0.5),
            LineTo(-0.5, -2.5),
            LineTo(0.5, -2.5)
        ]))
        self.addHole(0, 2, 0.195)
        self.addHole(0, -2, 0.195)


class CoverPlate(Part):
	def __init__(self):
		self.add(Path([
			MoveTo(0, 7),
			LineTo(0, 6),
			LineTo(0.5, 6),
			LineTo(1.5, 5),
			Arc(2, 5, 0.5, 180, 360),
			LineTo(2.5, 5),
			LineTo(4, 5),
			LineTo(4, 2),
			LineTo(2.5, 2),
			Arc(2, 2, 0.5, 0, 180),
			LineTo(1.5, 2),
			LineTo(0.5, 1),
			LineTo(0, 1),
			LineTo(0, 0),
			LineTo(1, 0),
			LineTo(1, 0.5),
			LineTo(2, 1.5),
			LineTo(4.5, 1.5),
			LineTo(4.5, 5.5),
			LineTo(2, 5.5),
			LineTo(1, 6.5),
			LineTo(1, 7),
			LineTo(0, 7)
		]))
		self.addHole(2, 2, 0.250)
		self.addHole(2, 5, 0.250)


gear1 = HPGLPart("gear.plt").bottomLeft()
gear2 = gear1.clone().dropPath(0).add(
    Hexagon.fromSize(7./16).translate(gear1.center()))

motorPlate = MotorPlate()

xoffset = gear1.getBbox().getMaxX()
yoffset = gear1.getBbox().getMaxY()
motorPlate = motorPlate.bottomLeft().translate(Vector(xoffset, 0))
xoffset2 = motorPlate.getBbox().getMaxX()
gearPlate = GearPlate().bottomLeft().translate(Vector(xoffset2, 0))
motorPlate = motorPlate.translate(Vector(0, 1))
gearPlate = gearPlate.translate(Vector(-1.5, 0))
xoffset3 = gearPlate.getBbox().getMaxX()

coverPlate = CoverPlate().rotate(90).bottomLeft().translate(Vector(3, 7))

support1 = RectangleMinusCorner(1, 1).bottomLeft().translate(Vector(5, 7.5))
support2 = RectangleMinusCorner(1, 1).bottomLeft().translate(Vector(6, 7.5))
support3 = Rectangle(4, 0.5).bottomLeft().translate(Vector(5, 7))

everything = Part()
everything.add(gear1)
everything.add(gear2.translate(Vector(0, yoffset)))
everything.add(gear2.translate(Vector(0, 2 * yoffset)))
everything.add(motorPlate)
everything.add(gearPlate)
everything.add(coverPlate)
everything.add(support1)
everything.add(support2)
everything.add(support3)

if 'only' in sys.argv[1:]:
	everything = Part()
	everything.add(gearPlate.bottomLeft().translate(1, 1))

if 'grid' in sys.argv[1:]:
	everything.addGrid()

if 'small' in sys.argv[1:]:
    everything = everything.scale(0.5).translate(1, 1)

if 'info' in sys.argv[1:]:
	print everything.getInfo()
	raise SystemExit

print "%!PS"
print everything.toPostscript()
print "showpage"
