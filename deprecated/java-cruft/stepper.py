import sys
sys.path.append("target/Parts-0.0.1-SNAPSHOT.jar")
from net.willware.parts import *   # NOQA


class StepperNEMA23(Part):
    def __init__(self):
        super(Part, self).__init__()
        if False:
            p = ColoredPath().setColor(1, 0, 0)
            p.add(0, 0, "moveto")
            p.add(0, 2.36, "lineto")
            p.add(2.36, 2.36, "lineto")
            p.add(2.36, 0, "lineto")
            p.add(0, 0, "lineto")
            self.add(p)
        self.addHole(1.190, 1.190, 0.25)
        self.addHole(0.262, 0.262, 0.195)
        self.addHole(0.262, 2.118, 0.195)
        self.addHole(2.118, 0.262, 0.195)
        self.addHole(2.118, 2.118, 0.195)
        self.add(NamedPoint("Motor axle", 1.190, 1.190))
