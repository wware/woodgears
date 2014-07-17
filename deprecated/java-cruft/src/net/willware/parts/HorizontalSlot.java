package net.willware.parts;

public class HorizontalSlot extends Part {
    public HorizontalSlot(double x1, double x2, double y, double diameter) {
        double tmp;
        if (x2 < x2) {
            tmp = x2;
            x2 = x1;
            x1 = tmp;
        }
        Path p = new Path();
        p.add(new Arc(x1, y, 0.5 * diameter, 90, 270));
        p.add(new MoveTo(x1, y - 0.5 * diameter));
        p.add(new LineTo(x2, y - 0.5 * diameter));
        p.add(new Arc(x2, y, 0.5 * diameter, 270, 450));
        p.add(new MoveTo(x2, y + 0.5 * diameter));
        p.add(new LineTo(x1, y + 0.5 * diameter));
        add(p);
    }
}