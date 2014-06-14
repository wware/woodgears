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

Download a reasonably recent
[Jython installer jar file](http://sourceforge.net/projects/jython/files/jython/2.5.2/jython_installer-2.5.2.jar/download)
and run the installer. It's convenient to just put the installation in
a subdirectory of your home directory (e.g. /Users/you/jython2.5.2 or
/home/you/jython2.5.2) and then copy the jython.jar file into the lib/ directory.

Make sure you have [a Java JDK](http://en.wikipedia.org/wiki/Java_(programming_language))
and [Maven](http://maven.apache.org/) installed, and type
```bash
mvn clean package
```
to build the Java code into a jar file. To run the script, type
```bash
java -jar lib/jython.jar mygears.py [args...]
```
