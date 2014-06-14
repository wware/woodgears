package net.willware.parts;

public class Matrix {
	private double a, b, c, d;
	public Matrix(double a, double b, double c, double d) {
		this.a = a;
		this.b = b;
		this.c = c;
		this.d = d;
	}
	public Vector apply(Vector v) {
		return new Vector(a * v.x + b * v.y, c * v.x + d * v.y);
	}
}
