package net.willware.parts;

import java.util.Formatter;
import java.util.Locale;

public class Vector extends Element {
	double x, y;
	public Vector(double x, double y) {
		this.x = x;
		this.y = y;
	}
	public String toString() {
		StringBuilder sb = new StringBuilder();
		Formatter formatter = new Formatter(sb, Locale.US);
		formatter.format("<%.3f %.3f>", x, y);
		return sb.toString();
	}
	public double getX() { return x; }
	public double getY() { return y; }
	public Bbox getBbox() {
		return new Bbox(x, x, y, y);
	}
	@Override
	public Element clone() {
		return new Vector(x, y);
	}
	@Override
	public Element translate(Vector v) {
		return new Vector(x + v.x, y + v.y);
	}
	@Override
	public Element rotate(double degrees) {
		double c = Math.cos(degrees * RADIANS_PER_DEGREE),
			s = Math.sin(degrees * RADIANS_PER_DEGREE);
		return new Vector(c * x - s * y, s * x + c * y);
	}
	@Override
	public Element scale(double scalar) {
		return new Vector(scalar * x, scalar * y);
	}
}
