package net.willware.parts;

import java.util.Formatter;
import java.util.Locale;

public class MoveTo implements PostscriptElement {

	Vector vec;
	
	public MoveTo(Vector v) {
		this.vec = v;
	}

	public MoveTo(double x, double y) {
		this.vec = new Vector(x, y);
	}

	@Override
	public Bbox getBbox() {
		return vec.getBbox();
	}

	@Override
	public String toPostscript() {
		StringBuilder sb = new StringBuilder();
		Formatter formatter = new Formatter(sb, Locale.US);
		formatter.format("%.2f %.2f moveto\n", POSTSCRIPT_DPI * vec.x, POSTSCRIPT_DPI * vec.y);
		return sb.toString();
	}

	@Override
	public Element clone() {
		return new MoveTo((Vector) vec.clone());
	}

	@Override
	public Element translate(Vector v) {
		return new MoveTo((Vector) vec.translate(v));
	}

	@Override
	public Element rotate(double degrees) {
		return new MoveTo((Vector) vec.rotate(degrees));
	}

	@Override
	public Element scale(double scalar) {
		return new MoveTo((Vector) vec.scale(scalar));
	}

	public static MoveTo make(double x, double y) {
		return new MoveTo(new Vector(x, y));
	}
}