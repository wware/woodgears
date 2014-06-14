package net.willware.parts;

import java.util.ArrayList;
import java.util.List;

public class Path implements PostscriptElement {

	private ArrayList<PostscriptElement> elements = new ArrayList<PostscriptElement>();
	protected Bbox bbox = null;

	public Path add(double x, double y, String op) {
		if ("lineto".equals(op))
			add(new LineTo(new Vector(x, y)));
		else if ("moveto".equals(op))
			add(new MoveTo(new Vector(x, y)));
		else
			throw new RuntimeException(op + "?");
		return this;
	}

	public Path add(PostscriptElement e) {
		if (e instanceof Path) {
			throw new RuntimeException("Do not add a Path to another Path");
		}
		elements.add(e);
		growBbox(e);
		return this;
	}

	public Path() {
	}

	public Path(List<PostscriptElement> lst) {
		for (PostscriptElement pe : lst) {
			add(pe);
		}
	}

	void growBbox(PostscriptElement e) {
		Bbox b = e.getBbox();
		bbox = (bbox == null) ? b : bbox.grow(b);
	}

	private Vector centerFromBbox() {
		return new Vector(0.5 * (bbox.getMinX() + bbox.getMaxX()),
			0.5 * (bbox.getMinY() + bbox.getMaxY()));
	}

	public Vector center() {
		return (bbox == null) ? null : centerFromBbox();
	}

	public int size() {
		return elements.size();
	}
	
	@Override
	public Bbox getBbox() {
		return bbox;
	}

	private interface Tweaker {
		PostscriptElement tweak(PostscriptElement e);
	}

	protected Path makeEmpty() {
		return new Path();
	}

	private Path tweak(Tweaker tw) {
		Path p = makeEmpty();
		p.bbox = null;
		for (PostscriptElement e : elements) {
			p.add(tw.tweak(e));
		}
		return p;
	}
	
	@Override
	public Element clone() {
		return tweak(new Tweaker() {
			public PostscriptElement tweak(PostscriptElement e) {
				return (PostscriptElement) e.clone();
			}
		});
	}

	@Override
	public Element translate(final Vector v) {
		return tweak(new Tweaker() {
			public PostscriptElement tweak(PostscriptElement e) {
				return (PostscriptElement) e.translate(v);
			}
		});
	}

	@Override
	public Element rotate(final double degrees) {
		return tweak(new Tweaker() {
			public PostscriptElement tweak(PostscriptElement e) {
				return (PostscriptElement) e.rotate(degrees);
			}
		});
	}

	@Override
	public Element scale(final double scalar) {
		return tweak(new Tweaker() {
			public PostscriptElement tweak(PostscriptElement e) {
				return (PostscriptElement) e.scale(scalar);
			}
		});
	}

	@Override
	public String toPostscript() {
		StringBuilder sb = new StringBuilder();
		for (PostscriptElement e : elements) {
			sb.append(e.toPostscript());
		}
		sb.append("stroke\n");
		return sb.toString();
	}
}
