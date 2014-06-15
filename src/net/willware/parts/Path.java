package net.willware.parts;

import java.util.ArrayList;
import java.util.List;

public class Path extends Element {

	private ArrayList<Element> elements = new ArrayList<Element>();

	public Element add(double x, double y, String op) {
		if ("lineto".equals(op))
			add(new LineTo(new Vector(x, y)));
		else if ("moveto".equals(op))
			add(new MoveTo(new Vector(x, y)));
		else
			throw new RuntimeException(op + "?");
		return this;
	}

	public Element add(Element e) {
		if (e instanceof Path) {
			throw new RuntimeException("Do not add a Path to another Path");
		}
		return _add(e);
	}

	public Path() {
	}

	public Path(List<Element> lst) {
		for (Element pe : lst) {
			add(pe);
		}
	}

	public int size() {
		return elements.size();
	}
	
	@Override
	public ArrayList<Element> getSubElements() {
		return elements;
	}

	@Override
	protected Element makeEmpty() {
		return new Path();
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
		for (Element e : elements) {
			sb.append(e.toPostscript());
		}
		sb.append("stroke\n");
		return sb.toString();
	}
}
