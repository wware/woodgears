Gears in laser-cut plywood
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
