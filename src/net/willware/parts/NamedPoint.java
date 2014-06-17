package net.willware.parts;

import java.util.Locale;
import java.util.Formatter;

public class NamedPoint extends Vector {
	String name;
    public NamedPoint(String name, double x, double y) {
    	super(x, y);
        this.name = name;
    }
    public boolean isInformational() {
        return true;
    }

    @Override
    public Element clone() {
        return new NamedPoint(name, x, y);
    }
    @Override
    public Element translate(Vector v) {
        return new NamedPoint(name, x + v.x, y + v.y);
    }
    @Override
    public Element rotate(double degrees) {
        double c = Math.cos(degrees * RADIANS_PER_DEGREE),
            s = Math.sin(degrees * RADIANS_PER_DEGREE);
        return new NamedPoint(name, c * x - s * y, s * x + c * y);
    }
    @Override
    public Element scale(double scalar) {
        return new NamedPoint(name, scalar * x, scalar * y);
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        Formatter formatter = new Formatter(sb, Locale.US);
        formatter.format("<\"%s\" %.3f %.3f>", name, x, y);
        return sb.toString();
    }
}