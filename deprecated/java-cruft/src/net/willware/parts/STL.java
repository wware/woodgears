package net.willware.parts;

import java.util.Locale;
import java.util.Formatter;
import java.util.ArrayList;

class STL {

    public static final double MM_PER_INCH = 25.4;

    private ArrayList<Facet> facets = new ArrayList<Facet>();
    private String name;
    private Element previous;

    public STL(String name) {
        this.name = name;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("solid ");
        sb.append(name);
        sb.append("\n");
        for (Facet facet : facets) {
            sb.append(facet);
        }
        sb.append("endsolid\n");
        return sb.toString();
    }

    class Vector3 {
        protected double x, y, z;
        public Vector3(double x, double y, double z) {
            this.x = x;
            this.y = y;
            this.z = z;
        }
        public String toString() {
            StringBuilder sb = new StringBuilder();
            Formatter formatter = new Formatter(sb, Locale.US);
            formatter.format("%.2f %.2f %.2f",
                MM_PER_INCH * x, MM_PER_INCH * y, MM_PER_INCH * z);
            return sb.toString();
        }
    }

    class Vertex extends Vector3 {
        public Vertex(double x, double y, double z) {
            super(x, y, z);
            if (x < 0.0 || y < 0.0 || z < 0.0) {
                throw new RuntimeException("all coordinates of a Vertex must be non-negative");
            }
        }
        public String toString() {
            return "      vertex " + super.toString() + "\n";
        }
    }

    class Facet {
        Vertex v1, v2, v3;
        Vector3 normal;
        public Facet(Vertex v1, Vertex v2, Vertex v3, Vector3 normal) {
            this.v1 = v1;
            this.v2 = v2;
            this.v3 = v3;
            this.normal = normal;
        }
        public String toString() {
            StringBuilder sb = new StringBuilder();
            sb.append("  facet normal ");
            sb.append(normal);
            sb.append("\n");
            sb.append("    outer loop\n");
            sb.append(v1);
            sb.append(v2);
            sb.append(v3);
            sb.append("    endloop\n");
            sb.append("  endfacet\n");
            return sb.toString();
        }
    }

    public STL extrude(Element current, double height) {
        LineTo prev, curr;
        if (current instanceof MoveTo) {
            previous = current;
        }
        else if (current instanceof LineTo) {
            if (previous == null || !(previous instanceof MoveTo)) {
                throw new RuntimeException("bad previous Element during STL extrusion");
            }
            prev = (LineTo) previous;
            curr = (LineTo) current;
            Vertex v1 = new Vertex(prev.getX(), prev.getY(), 0.0);
            Vertex v2 = new Vertex(curr.getX(), curr.getY(), height);
            Vertex v3 = new Vertex(prev.getX(), prev.getY(), 0.0);
            Vertex v4 = new Vertex(curr.getX(), curr.getY(), height);
            Vector3 normal = new Vector3(0.0, 0.0, 0.0);  // TODO
            facets.add(new Facet(v1, v2, v3, normal));
            facets.add(new Facet(v2, v3, v4, normal));
            previous = current;
        }
        else if (current instanceof Path || current instanceof Part) {
            for (Element e : current.getSubElements()) {
                extrude(e, height);
            }
        }
        else {
            throw new RuntimeException("cannot extrude " + current);
        }
        return this;
    }
}