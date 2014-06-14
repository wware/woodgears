package net.willware.parts;

public class StepperNEMA23 extends Part {

	public StepperNEMA23() {
		Path p = new ColoredPath().setColor(1, 0, 0);
		p.add(0, 0, "moveto");
		p.add(0, 2.36, "lineto");
		p.add(2.36, 2.36, "lineto");
		p.add(2.36, 0, "lineto");
		p.add(0, 0, "lineto");
		add(p);
		addHole(1.190, 1.190, 0.25);
		addHole(0.262, 0.262, 0.195);
		addHole(0.262, 2.118, 0.195);
		addHole(2.118, 0.262, 0.195);
		addHole(2.118, 2.118, 0.195);
	}
}