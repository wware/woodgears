package net.willware.parts;

import java.util.ArrayList;

public abstract class Element {

    public static final double POSTSCRIPT_DPI = 72;
    public static final double RADIANS_PER_DEGREE = Math.PI / 180;
    public static final double HPGL_DPI = 40 * 25.4;

    private Bbox bbox = null;

    public abstract Element clone();
    public abstract Element translate(Vector v);
    public abstract Element rotate(double degrees);
    public abstract Element scale(double scalar);
    public String toHPGL() {
        throw new UnsupportedOperationException();
    }
    public String toPostscript() {
        throw new UnsupportedOperationException();
    }

    private Vector centerFromBbox() {
        return new Vector(0.5 * (bbox.getMinX() + bbox.getMaxX()),
            0.5 * (bbox.getMinY() + bbox.getMaxY()));
    }

    public Bbox getBbox() {
        return bbox;
    }

    public Vector center() {
        return (bbox == null) ? null : centerFromBbox();
    }

    protected Element _add(Element e) {
        getSubElements().add(e);
        growBbox(e);
        return this;
    }

    protected void growBbox(Element e) {
        Bbox b = e.getBbox();
        bbox = (bbox == null) ? b : bbox.grow(b);
    }

    public ArrayList<Element> getSubElements() {
        throw new UnsupportedOperationException();
    }
    protected Element makeEmpty() {
        throw new UnsupportedOperationException();
    }

    protected interface Tweaker {
        Element tweak(Element e);
    }

    protected Element apply(Tweaker tw) {
        Element newguy = makeEmpty();
        newguy.bbox = null;
        for (Element e : getSubElements()) {
            newguy._add(tw.tweak(e));
        }
        return newguy;
    }

}
