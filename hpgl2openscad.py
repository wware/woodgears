#!/usr/bin/env python
# -*- coding: utf-8 -*-

("""
Usage:
  CMD [-D | --debug] (-T | --test)
  CMD [-D | --debug] [-m | --mm] """ +
    """[-n <NAME> | --name <NAME>] (-f | --file) <FILENAME>

This script is used to create OpenSCAD modules from the HPGL files generated by
the Matthias Wandel's very beautiful Gear Template Generator, at
https://woodgears.ca/gear_cutting/template.html

Having created a gear file (typically with a ".plt" extension) you can pipe the
standard output of this script to a ".scad" file and do something like this.

    $ ./hpgl2openscad.py -f woodgears/gear.plt > foo.scad
    $ cat > bar.scad
    use <foo.scad>;
    Gear();
    translate([3,0,0]) {
        Gear();
    }
    ^D
    $ /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD bar.scad

""")

import docopt
import logging
import sys

logger = logging.getLogger('hpgl2openscad')


class HpglInterpreter(object):

    def __init__(self):
        self.paths = []
        self._use_inches = True

    def read(self, inf, scale=1.0):
        scale /= 40.0    # HPGL dots per millimeter
        if self._use_inches:
            scale /= 25.4
        active = False
        p = []
        while True:
            line = inf.readline()
            # logger.debug(line.strip())
            if not line:
                break
            line = line.strip()
            if line == 'SP1;':
                active = True
            elif line.startswith('SP'):
                active = False
            elif active and line.startswith('PU '):
                self.add_path(p)
                p = []
                fields = line.replace('a', 'A')[3:-1].split(',')
                x, y = map(int, fields[:2])
                mt = self.create_move_to(scale * x, scale * y)
                p.append(mt)
            elif active and line.startswith('PD '):
                fields = line.replace('a', 'A')[3:-1].split(',')
                x, y = map(int, fields[:2])
                lt = self.create_line_to(scale * x, scale * y)
                p.append(lt)
        if len(p) > 0:
            self.add_path(p)

    def units(self):
        return self._use_inches and 'inches' or 'mm'

    def add_path(self, p):
        logger.debug('add_path:' + repr(p))
        self.paths.append(p)

    def create_move_to(self, x, y):
        # logger.debug('create_move_to:{0}:{1}'.format(x, y))
        return ('moveTo', x, y)

    def create_line_to(self, x, y):
        # logger.debug('create_line_to:{0}:{1}'.format(x, y))
        return ('lineTo', x, y)


class OpenSCADPolygon(HpglInterpreter):

    def __init__(self, name='Gear'):
        super(OpenSCADPolygon, self).__init__()
        self.name = name

    def add_path(self, p):
        p = p[1:]
        if p:
            self.paths.append(p)

    def create_move_to(self, x, y):
        # OpenSCAD polygons use closed paths and do not repeat the beginning
        # and ending point as HPGL does, so return a None which will later be
        # removed.
        return None

    def create_line_to(self, x, y):
        return [x, y]

    def __repr__(self):
        all_points = reduce(lambda x, y: x + y, self.paths)
        sum_of_points = reduce(lambda p1, p2:
                               (p1[0] + p2[0], p1[1] + p2[1]),
                               all_points)
        center = (sum_of_points[0] / len(all_points),
                  sum_of_points[1] / len(all_points))
        all_points = map(
            lambda p, center=center: [p[0] - center[0], p[1] - center[1]],
            all_points
        )
        indices = []
        n = 0
        for path in self.paths:
            N = n + len(path)
            indices.append(range(n, N))
            n = N
        a, b = repr(all_points), repr(indices)
        quarter_inch = 0.25
        if not self._use_inches:
            quarter_inch *= 25.4
        return """module {0}() {1} linear_extrude(height={2}, center=true)
            polygon(points={3}, paths={4});{5}"""\
            .format(self.name, "{", quarter_inch, a, b, "}") + \
            """\n{0}();\n""".format(self.name)


def main():
    ch = logging.StreamHandler()
    ch.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - " +
                          "%(levelname)s - %(message)s")
    )
    logger.addHandler(ch)

    args = docopt.docopt(__doc__.replace('CMD', sys.argv[0]))

    if args['-D'] or args['--debug']:
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
        logger.debug('hello')

    if args['-T'] or args['--test']:
        import doctest
        # verbose=True can be useful
        failure_count, test_count = \
            doctest.testmod(optionflags=doctest.ELLIPSIS)
        sys.exit(failure_count)

    if args['-n'] or args['--name']:
        name = args['<NAME>']
    else:
        name = 'Gear'

    if args['-f'] or args['--file']:
        inf = open(args['<FILENAME>'])
    else:
        inf = sys.stdin

    interp = OpenSCADPolygon(name)
    if args['-m'] or args['--mm']:
        interp._use_inches = False
    interp.read(inf)
    print interp


if __name__ == '__main__':
    main()