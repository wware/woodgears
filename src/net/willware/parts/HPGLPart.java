package net.willware.parts;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class HPGLPart extends Part {

	public HPGLPart() {
	}

	public HPGLPart(String filename) throws IOException {
		read(filename);
	}

	public Part read(String filename) throws IOException {
		return read(new FileInputStream(filename));
	}

	public Part read(InputStream ins) throws IOException {
		BufferedReader buffer = new BufferedReader(new InputStreamReader(ins));
		Path p = new Path();
		double scale = 1.0 / (25.4 * 40);
		boolean active = false;
		while (true) {
			String line = buffer.readLine();
			if (line == null) {
				break;
			} else if ("SP1;".equals(line)) {
				active = true;
			} else if (line.startsWith("SP")) {
				active = false;
			} else if (active && line.startsWith("PU ")) {
				if (p.size() > 0) {
					add(p);
					p = new Path();
				}
				String[] fields = line.replace(";", "").substring(3).split(",");
				int x = Integer.parseInt(fields[0]), y = Integer.parseInt(fields[1]);
				p.add(MoveTo.make(scale * x, scale * y));
			} else if (active && line.startsWith("PD ")) {
				String[] fields = line.replace(";", "").substring(3).split(",");
				int x = Integer.parseInt(fields[0]), y = Integer.parseInt(fields[1]);
				p.add(LineTo.make(scale * x, scale * y));
			}
		}
		if (p.size() > 0) {
			add(p);
		}
		return this;
	}
}
