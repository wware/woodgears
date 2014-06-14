package net.willware.parts;

public interface Element {
	public static final double POSTSCRIPT_DPI = 72;
	public static final double RADIANS_PER_DEGREE = Math.PI / 180;
	Bbox getBbox();
	Element clone();
	Element translate(Vector v);
	Element rotate(double degrees);
	Element scale(double scalar);
}
