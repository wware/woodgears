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

	ArrayList<Path> paths = new ArrayList<Path>();

	public Part add(Path p) {
		paths.add(p);
		growBbox(p);
		return this;
	}

	public Part add(Part p) {
		for (Path path : p.paths) {
			add(path);
		}
		return this;
	}

	public Part bottomLeft() {
		Bbox b = getBbox();
		return (Part) translate(new Vector(-b.getMinX(), -b.getMinY()));
	}

	public Part centerAtOrigin() {
		Vector c = center();
		return (Part) translate(new Vector(-c.getX(), -c.getY()));
	}

	private interface Tweaker {
		Path tweak(Path e);
	}

	private static String getStackTrace(final Throwable throwable) {
	     final StringWriter sw = new StringWriter();
	     final PrintWriter pw = new PrintWriter(sw, true);
	     throwable.printStackTrace(pw);
	     return sw.getBuffer().toString();
	}

	private Part tweak(Tweaker tw) {
		Part p = new Part();
		p.bbox = null;
		for (Path e : paths) {
			p.add(tw.tweak(e));
		}
		return p;
	}

	@Override
	public Element clone() {
		return tweak(new Tweaker() {
			public Path tweak(Path e) {
				return (Path) e.clone();
			}
		});
	}

	@Override
	public Element translate(final Vector v) {
		return tweak(new Tweaker() {
			public Path tweak(Path e) {
				return (Path) e.translate(v);
			}
		});
	}

	@Override
	public Element rotate(final double degrees) {
		return tweak(new Tweaker() {
			public Path tweak(Path e) {
				return (Path) e.rotate(degrees);
			}
		});
	}

	@Override
	public Element scale(final double scalar) {
		return tweak(new Tweaker() {
			public Path tweak(Path e) {
				return (Path) e.scale(scalar);
			}
		});
	}

	@Override
	public String toPostscript() {
		StringBuilder sb = new StringBuilder();
		for (Path e : paths) {
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
