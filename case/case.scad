// Texas Wildlife ID - 3D Printed Enclosure v4 with pan-tilt support
enclosure_width = 150;
enclosure_depth = 120;
enclosure_height = 60;
wall_thickness = 3;
base_thickness = 4;
lid_thickness = 3;
standoff_height = 10;

mount_hole_dia = 3.2;
mount_grid = [[20,20],[130,20],[20,100],[130,100]];

camera_hole_dia = 25;
cable_gland_dia = 12;

// Solar panel bracket params
solar_panel_width = 200;
solar_panel_depth = 150;
bracket_length = 80;
bracket_thickness = 5;

// Thermal management params
fan_dia = 40;
fan_thickness = 10;
chimney_height = 40;
heatsink_fin_height = 15;

// Pan-tilt mount params
pan_tilt_base_dia = 80;
pan_tilt_mount_height = 20;

module base(){
    difference(){
        union(){
            translate([0,0,enclosure_height/2]) cube([enclosure_width, enclosure_depth, enclosure_height], center=true);
            translate([0,0,-enclosure_height/2 + base_thickness/2]) cube([enclosure_width, enclosure_depth, base_thickness], center=true);
        }
        translate([0,0,0]) cube([enclosure_width-2*wall_thickness, enclosure_depth-2*wall_thickness, enclosure_height], center=true);
        for(p = mount_grid){
            translate([p[0]-enclosure_width/2, p[1]-enclosure_depth/2, -enclosure_height/2]) cylinder(h=enclosure_height+10, d=mount_hole_dia, center=false);
        }
        // Camera cutout
        translate([enclosure_width/2 - 15, 0, enclosure_height/2 - wall_thickness])
        rotate([90,0,0])
        cylinder(h=wall_thickness+5, d=camera_hole_dia, center=true);
        // Cable glands
        translate([-enclosure_width/2 + 20, 0, -enclosure_height/2 + wall_thickness])
        rotate([90,0,90])
        cylinder(h=wall_thickness+5, d=cable_gland_dia, center=true);
        translate([enclosure_width/2 - 20, 0, -enclosure_height/2 + wall_thickness])
        rotate([90,0,90])
        cylinder(h=wall_thickness+5, d=cable_gland_dia, center=true);
    }
}

module lid(){
    difference(){
        translate([0,0,enclosure_height + lid_thickness/2]) cube([enclosure_width, enclosure_depth, lid_thickness], center=true);
        translate([0,0,enclosure_height + lid_thickness/2 - 0.5])
        cube([enclosure_width-2*wall_thickness, enclosure_depth-2*wall_thickness, lid_thickness+2], center=true);
    }
}

module pi_standoffs(){
    translate([-20, -10, -enclosure_height/2 + base_thickness + standoff_height/2]){
        for(i=[0:3]){
            x = i%2==0 ? -42.5 : 42.5;
            y = i<2 ? -28 : 28;
            translate([x, y, 0]) cylinder(h=standoff_height, d=6);
        }
    }
}

module vents(){
    for(i=[0:3]){
        translate([-enclosure_width/2+25 + i*35, enclosure_depth/2 - wall_thickness/2, -enclosure_height/2 + 15])
        cube([25, wall_thickness, 8], center=true);
    }
}

module fan_mount(){
    translate([0, -enclosure_depth/2 + wall_thickness, enclosure_height/2 - wall_thickness])
    rotate([90,0,0])
    difference(){
        cylinder(h=wall_thickness+5, d=fan_dia+4, center=true);
        cylinder(h=wall_thickness+10, d=fan_dia, center=true);
    }
}

module chimney(){
    translate([0, -enclosure_depth/2 - 10, enclosure_height/2])
    rotate([90,0,0])
    cylinder(h=chimney_height, d=fan_dia+6, center=false);
}

module heatsink_fins(){
    for(i=[0:5]){
        translate([ -enclosure_width/2 + 20 + i*25, 0, enclosure_height/2 + lid_thickness])
        cube([15, enclosure_depth-20, heatsink_fin_height], center=true);
    }
}

module pan_tilt_mount(){
    translate([0, enclosure_depth/2 + pan_tilt_mount_height/2, -enclosure_height/2])
    difference(){
        cylinder(h=pan_tilt_mount_height, d=pan_tilt_base_dia, center=true);
        translate([0,0,0]) cylinder(h=pan_tilt_mount_height+2, d=20, center=true);
        for(a=[0:3]){
            rotate([0,0,a*90])
            translate([pan_tilt_base_dia/2 - 10, 0, 0])
            cylinder(h=pan_tilt_mount_height+2, d=mount_hole_dia, center=true);
        }
    }
}

module solar_bracket(){
    translate([enclosure_width/2 + bracket_length/2, 0, -enclosure_height/2])
    difference(){
        union(){
            cube([bracket_thickness, bracket_thickness, enclosure_height + 20], center=false);
            translate([0, 0, enclosure_height + 20])
            cube([bracket_length, bracket_thickness, bracket_thickness], center=false);
        }
        translate([bracket_thickness/2, bracket_thickness/2, 10])
        cylinder(h=enclosure_height+30, d=mount_hole_dia, center=false);
    }
}

module cable_gland(){
    difference(){
        cylinder(h=15, d=20, center=false);
        translate([0,0,2]) cylinder(h=13, d=12, center=false);
        translate([0,0,2]) cylinder(h=13, d=6, center=false);
    }
}

base();
pi_standoffs();
vents();
fan_mount();
chimney();
heatsink_fins();
pan_tilt_mount();
lid();
solar_bracket();
// cable_gland(); // uncomment to preview
