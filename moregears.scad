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
// use <gear120.scad>;

module StepperGear() {
    difference() {
        union() {
            translate([0,0,-0.125])
                    cylinder(h=0.25, r=0.2, $fn=8);
            Gear10();
        }
        translate([0,0,-0.13]) {
            intersection() {
                cylinder(h=0.35, r=0.125, $fn=40);
                translate([-0.125, -0.125, 0]) {
                    cube([0.228, 0.25, 0.35]);
                }
            }
        }
    }
}

module HexNutGear() {
    difference() {
        Gear10();
        intersection_for(n = [1 : 3]) {
            rotate([0, 0, n * 60]) {
                translate([-0.21875,-0.5,-0.5])
                    cube([0.4375,1,1]);
            }
        }
    }
}

projection(cut = true) {
    import("annular_gear.stl");
	StepperGear();
	translate([1.2, 0, 0]) HexNutGear();
	translate([0, 1.2, 0]) HexNutGear();
	translate([1.2, 1.2, 0]) HexNutGear();
}

module TorusGear() {
    difference() {
        Gear120();
        Gear100();
    }
}

// TorusGear();
