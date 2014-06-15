import sys
sys.path.append("target/Parts-0.0.1-SNAPSHOT.jar")
from net.willware.parts import *
from stepper import StepperNEMA23


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


gear1 = HPGLPart("gear.plt").bottomLeft()
gear2 = gear1.clone().dropPath(0).add(Hexagon.fromSize(7./16).translate(gear1.center()))

motorPlate = MotorPlate()

xoffset = gear1.getBbox().getMaxX()
yoffset = gear1.getBbox().getMaxY()
motorPlate = motorPlate.bottomLeft().translate(Vector(xoffset, 0))
xoffset2 = motorPlate.getBbox().getMaxX()
gearPlate = GearPlate().bottomLeft().translate(Vector(xoffset2, 0))

everything = Part()
everything.add(gear1)
everything.add(gear2.translate(Vector(0, yoffset)))
everything.add(gear2.translate(Vector(0, 2 * yoffset)))
everything.add(motorPlate.translate(Vector(0, 1)))
everything.add(gearPlate.translate(Vector(-1.5, 0)))

if 'small' in sys.argv[1:]:
	everything = everything.scale(0.5)

print "%!PS"
print everything.toPostscript()
print "showpage"
