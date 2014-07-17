package net.willware.parts;

import java.util.Formatter;
import java.util.Locale;

public class MoveTo extends LineTo {

    public MoveTo(Vector v) {
        super(v);
    }

    public MoveTo(double x, double y) {
        super(x, y);
    }

    @Override
    protected String getPostscriptCommand() {
        return "moveto";
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
