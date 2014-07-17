package net.willware.parts;

import java.util.Formatter;
import java.util.Locale;

public class Arc extends Element {

    Vector center;
    double radius, angle1, angle2;

    public Arc(Vector center, double radius, double angle1, double angle2) {
        this.center = center;
        this.radius = radius;
        this.angle1 = angle1;
        this.angle2 = angle2;
    }

    public Arc(double x, double y, double radius, double angle1, double angle2) {
        this.center = new Vector(x, y);
        this.radius = radius;
        this.angle1 = angle1;
        this.angle2 = angle2;
    }

    @Override
    public Bbox getBbox() {
        Bbox b = center.getBbox();
        // this is over-conservative, you don't need the full box
        // if you don't have a complete circle
        return new Bbox(
            b.getMinX() - radius,
            b.getMaxX() + radius,
            b.getMinY() - radius,
            b.getMaxY() + radius);
    }

    @Override
    public Element clone() {
        return new Arc((Vector) center.clone(), radius, angle1, angle2);
    }

    @Override
    public Element translate(Vector v) {
        return new Arc((Vector) center.translate(v), radius, angle1, angle2);
    }

    @Override
    public Element rotate(double degrees) {
        return new Arc((Vector) center.rotate(degrees), radius,
                angle1 + degrees, angle2 + degrees);
    }

    @Override
    public Element scale(double scalar) {
        return new Arc((Vector) center.scale(scalar), radius * scalar, angle1, angle2);
    }

    @Override
    public String toPostscript() {
        StringBuilder sb = new StringBuilder();
        Formatter formatter = new Formatter(sb, Locale.US);
        formatter.format("%.2f %.2f %.2f %.2f %.2f arc\n",
            POSTSCRIPT_DPI * center.x, POSTSCRIPT_DPI * center.y, POSTSCRIPT_DPI * radius, angle1, angle2);
        return sb.toString();
    }
}
