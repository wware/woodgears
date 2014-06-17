package net.willware.parts;

import java.util.Formatter;
import java.util.Locale;

public class ColoredPath extends Path {
    private double red, green, blue;

    public ColoredPath setColor(double r, double g, double b) {
        red = r;
        green = g;
        blue = b;
        return this;
    }

    @Override
    protected Element makeEmpty() {
        ColoredPath p = new ColoredPath();
        p.red = red;
        p.green = green;
        p.blue = blue;
        return p;
    }

    @Override
    public String toPostscript() {
        StringBuilder sb = new StringBuilder();
        Formatter formatter = new Formatter(sb, Locale.US);
        formatter.format("gsave %.2f %.2f %.2f setrgbcolor\n", red, green, blue);
        sb.append(super.toPostscript());
        sb.append("grestore\n");
        return sb.toString();
    }
}
