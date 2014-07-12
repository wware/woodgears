Mechanisms in laser-cut plywood
==

There is a [gear template
designer](http://woodgears.ca/gear_cutting/template.html) on
[woodgears.ca](http://woodgears.ca), a website dedicated to wooden gears and
other wooden mechanical things. The template designer takes various parameters
and produces patterns for cutting out gears from plywood or other materials.
The output format is [HPGL](http://en.wikipedia.org/wiki/HPGL), which uses
units of 1/40 mm. So the conversion to Postscript units is (72 / (25.4 * 40)).

The settings I used were two gears, both with 20 teeth, 10mm per gear tooth,
contact angle 25 degrees, 3 spokes, bore diameter 6.35 mm (1/4"). When I asked
for a print, I only got one gear but that's OK because they're identical. The
result is the file `gear.plt`.

There is some great information in the online material for Carnegie-Mellon's
[rapid prototyping course](http://www.cs.cmu.edu/~rapidproto/). Gear teeth
should have a shape described by an _involute_ curve described
[here](http://www.cs.cmu.edu/~rapidproto/mechanisms/chpt7.html). The fact that
this information is available online means that I can eventually put it in the
Python code and not need to go to the woodgears.ca website. And check out the
section on [rigid body
mechanics](http://www.cs.cmu.edu/~rapidproto/mechanisms/chpt4.html). Also,
there is info about stepper motor sizes
[here](http://www.piclist.com/techref/io/stepper/nemasizes.htm).

Initially I wanted to put together a little Python library that enables gears
to be copied and repositioned, and the center hole replace by a hexagonal
cutout for nuts. For my immediate need, the wrench size for the hex cutout is
7/16". This is the beginnings of a library like that. It looks like it may be
possible to do something a bit more ambitious.

Java and Jython
--

Download a reasonably recent [Jython installer jar
file](http://sourceforge.net/projects/jython/files/jython/2.5.2/jython_installer-2.5.2.jar/download)
and run the installer. It's convenient to follow the default and put the
installation in a subdirectory of your home directory.

Make sure you have [a Java JDK](http://en.wikipedia.org/wiki/Java_(programming_language))
and [Maven](http://maven.apache.org/) installed, and type
```bash
mvn clean package
```
to build the Java code into a jar file. To run the script, type
```bash
java -jar $HOME/jython2.5.2/jython.jar mygears.py [args...]
```

Java? Jython??? the hell was I thinking?
--

Let's try to borrow from what we learned working on
[geom3d.py](https://github.com/wware/proj-driver/blob/master/geom3d.py) in the
[proj-driver](https://github.com/wware/proj-driver) project. And if possible, unify these two projects.

For starters, `geom3d.py` has lovely classes for Vector and BBox, which could accomodate 2D geometry with
no trouble at all.

Actually let's just think about what we really need, rather than blindly reproducing everything here.

After some thought, I think unification is eminently practical. You can use OpenSCAD from the
[command line](http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_OpenSCAD_in_a_command_line_environment)
to generate an STL file, and I think a little bit of work can get everything up and running
that way. Rewrite the code that runs underneath `mygears.py`, and make it generate extruded polygons in
[OpenSCAD](http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem).

Generate Postscript?
--

*Postscript generation is no longer needed, see below.*

We need something that takes a bunch of 2D shapes in a
plane and produces Postscript. The code in `proj-driver` takes a STL file, which is a bunch of triangle is 3D
space, and computing their intersections with a line in the x-direction.

Let's start to envision another sort of slice operation to generate Postscript. As a plane cuts through a
bunch of triangles, you get a bunch of line segments. You could be stupid and just do `moveto lineto` for each
of them, but really you want to try to join them to form paths.

In a given Z plane, you compute all those line segments in an XY plane, and then
you partition the plane with a big square grid. Every (x,y) point goes in one square of the grid. You avoid
floating-point ambiguity by using `xmin - epsilon <= x < xmax - epsilon` as the membership criterion, where
epsilon is tiny.

Now you pick a line segment as random, and you try to grow it at both ends by finding other line segments that
connect to it, which is efficient because the partitioning has you looking at only a teeny number of candidates
each time. When you have a path, you remove those line segments from the line segment list and add that path
to a path list. You keep going until the line segment list is empty. Now you render all those paths in Postscript.

Maybe generate DXF instead of Postscript?
--

[Danger!awesome](http://dangerawesome.co/our-technology/)'s website says:

> We prefer .eps, .pdf, and .dxf files, though if needed we can work from a range of raster-based
> file formats for etching/engraving and vector-based file formats for etching/engraving and cutting.

OpenSCAD can
[generate DXF](http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#3D_to_2D_Projection)
from a slice of a 3D model.

Importing HPGL from Gear Generator
--

There is a 2D subsystem in OpenSCAD. Convert the HPGL to primitives. All I need to do is take the output of
Gear Generator and convert it to an OpenSCAD polygon, and extrude it to produce a 3D gear.
