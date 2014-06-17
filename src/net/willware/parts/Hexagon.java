package net.willware.parts;

public class Hexagon extends Part {
    public static final double SQRT3 = Math.sqrt(3);
    public Hexagon(double size) {
        double hsize = 0.5 * size;
        double asize = 0.5 * SQRT3 * size;
        Path p = new Path();
        p.add(new MoveTo(new Vector(-size, 0)));
        p.add(new LineTo(new Vector(-hsize, asize)));
        p.add(new LineTo(new Vector(hsize, asize)));
        p.add(new LineTo(new Vector(size, 0)));
        p.add(new LineTo(new Vector(hsize, -asize)));
        p.add(new LineTo(new Vector(-hsize, -asize)));
        p.add(new LineTo(new Vector(-size, 0)));
        add(p);
    }
    public static Hexagon fromSize(double size) {
        return new Hexagon(size / SQRT3);
    }
}
