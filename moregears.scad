/*
This would be for millimeters, but the stuff in this file is in inches.
./hpgl2openscad.py -m -n Gear10 -f gear10.plt > gear10.scad
./hpgl2openscad.py -m -n Gear100 -f gear100.plt > gear100.scad
./hpgl2openscad.py -m -n Gear120 -f gear120.plt > gear120.scad

So do this instead.
./hpgl2openscad.py -n Gear10 -f gear10.plt > gear10.scad
./hpgl2openscad.py -n Gear100 -f gear100.plt > gear100.scad
./hpgl2openscad.py -n Gear120 -f gear120.plt > gear120.scad
/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD moregears.scad -o foo.stl
*/

use <gear10.scad>;
use <gear100.scad>;
use <gear120.scad>;

module StepperGear() {
    scale([1,1,0.25]) {
        difference() {
            union() {
                translate([0,0,-0.5])
                        cylinder(h=1, r=0.2);
                Gear10();
            }
            translate([0,0,-0.5]) {
                intersection() {
                    cylinder(h=1, r=0.125, $fs=0.01);
                    translate([-0.125, -0.125, 0]) {
                        cube([0.228, 0.25, 1]);
                    }
                }
            }
        }
    }
}

// StepperGear();
// translate([3,0,0]) scale([1,1,0.25]) Gear10();

module TorusGear() {
    difference() {
        Gear120();
        Gear100();
    }
}

TorusGear();
