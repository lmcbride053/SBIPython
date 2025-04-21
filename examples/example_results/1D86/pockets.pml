# PyMOL visualization script for predicted binding pockets
bg_color white
hide everything
show cartoon
color gray80
pseudoatom pocket_0, pos=[20.594, 23.059, -12.174], color=red
show spheres, pocket_0
set sphere_scale, 1.0, pocket_0
pseudoatom pocket_1, pos=[8.935, 11.652, -10.422], color=orange
show spheres, pocket_1
set sphere_scale, 1.0, pocket_1
zoom
