package net.willware.parts;

import java.util.Formatter;
import java.util.Locale;

public class Bbox {
    private double minX, maxX, minY, maxY;
    public Bbox(double minX, double maxX, double minY, double maxY) {
        this.minX = minX;
        this.maxX = maxX;
        this.minY = minY;
        this.maxY = maxY;
    }
    public String toString() {
        StringBuilder sb = new StringBuilder();
        Formatter formatter = new Formatter(sb, Locale.US);
        formatter.format("<Bbox %.3f %.3f %.3f %.3f>", minX, maxX, minY, maxY);
        return sb.toString();
    }
    public double getMinX() { return minX; }
    public double getMaxX() { return maxX; }
    public double getMinY() { return minY; }
    public double getMaxY() { return maxY; }
    public Bbox grow(Bbox other) {
        return new Bbox(
            (minX < other.minX) ? minX : other.minX,
            (maxX > other.maxX) ? maxX : other.maxX,
            (minY < other.minY) ? minY : other.minY,
            (maxY > other.maxY) ? maxY : other.maxY);
    }
}
