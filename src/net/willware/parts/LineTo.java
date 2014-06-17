package net.willware.parts;

import java.util.Formatter;
import java.util.Locale;

public class LineTo extends Element {

    Vector vec;

    public LineTo(Vector v) {
        this.vec = v;
    }

    public LineTo(double x, double y) {
        this.vec = new Vector(x, y);
    }

    public double getX() {
        return vec.getX();
    }

    public double getY() {
        return vec.getY();
    }

    @Override
    public Bbox getBbox() {
        return vec.getBbox();
    }

    @Override
    public Element clone() {
        return new LineTo((Vector) vec.clone());
    }

    @Override
    public Element translate(Vector v) {
        return new LineTo((Vector) vec.translate(v));
    }

    @Override
    public Element rotate(double degrees) {
        return new LineTo((Vector) vec.rotate(degrees));
    }

    @Override
    public Element scale(double scalar) {
        return new LineTo((Vector) vec.scale(scalar));
    }

    protected String getPostscriptCommand() {
        return "lineto";
    }

    @Override
    public String toPostscript() {
        StringBuilder sb = new StringBuilder();
        Formatter formatter = new Formatter(sb, Locale.US);
        formatter.format("%.2f %.2f ", POSTSCRIPT_DPI * vec.x, POSTSCRIPT_DPI * vec.y);
        formatter.format(getPostscriptCommand());
        formatter.format("\n");
        return sb.toString();
    }

    public static LineTo make(double x, double y) {
        return new LineTo(new Vector(x, y));
    }
}
