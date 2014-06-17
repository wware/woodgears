package net.willware.parts;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.ArrayList;

public class Part extends Path {

    ArrayList<Element> paths = new ArrayList<Element>();

    public Element add(Element e) {
        if (!(e instanceof Path)) {
            throw new RuntimeException("Elements of a Part must be instances of Path");
        }
        return _add(e);
    }

    public Part bottomLeft() {
        Bbox b = getBbox();
        return (Part) translate(new Vector(-b.getMinX(), -b.getMinY()));
    }

    public Part centerAtOrigin() {
        Vector c = center();
        return (Part) translate(new Vector(-c.getX(), -c.getY()));
    }

    @Override
    protected Element makeEmpty() {
        return new Part();
    }

    @Override
    public ArrayList<Element> getSubElements() {
        return paths;
    }

    private static String getStackTrace(final Throwable throwable) {
         final StringWriter sw = new StringWriter();
         final PrintWriter pw = new PrintWriter(sw, true);
         throwable.printStackTrace(pw);
         return sw.getBuffer().toString();
    }

    @Override
    public Element clone() {
        return apply(new Tweaker() {
            public Element tweak(Element e) {
                return e.clone();
            }
        });
    }

    @Override
    public Element translate(final Vector v) {
        return apply(new Tweaker() {
            public Element tweak(Element e) {
                return e.translate(v);
            }
        });
    }

    @Override
    public Element rotate(final double degrees) {
        return apply(new Tweaker() {
            public Element tweak(Element e) {
                return e.rotate(degrees);
            }
        });
    }

    @Override
    public Element scale(final double scalar) {
        return apply(new Tweaker() {
            public Element tweak(Element e) {
                return e.scale(scalar);
            }
        });
    }

    @Override
    public String toPostscript() {
        StringBuilder sb = new StringBuilder();
        for (Element e : paths) {
            sb.append(e.toPostscript());
        }
        return sb.toString();
    }

    public Part dropPath(int i) {
        paths.remove(i);
        return this;
    }

    public void addHole(double x, double y, double diameter) {
        Path p = new Path();
        p.add(new Arc(new Vector(x, y), 0.5 * diameter,  0, 360));
        add(p);
    }
}
