# PyMOL visualization script for predicted binding pockets
bg_color white
hide everything
show cartoon
color gray80
pseudoatom pocket_0, pos=[44.418, 26.818, -3.855], color=red
show spheres, pocket_0
set sphere_scale, 1.0, pocket_0
pseudoatom pocket_1, pos=[57.441, -2.811, 28.463], color=orange
show spheres, pocket_1
set sphere_scale, 1.0, pocket_1
zoom
