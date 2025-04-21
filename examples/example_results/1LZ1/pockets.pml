# PyMOL visualization script for predicted binding pockets
bg_color white
hide everything
show cartoon
color gray80
pseudoatom pocket_0, pos=[7.630, 24.939, 13.015], color=red
show spheres, pocket_0
set sphere_scale, 1.0, pocket_0
pseudoatom pocket_1, pos=[25.626, 9.258, 39.878], color=orange
show spheres, pocket_1
set sphere_scale, 1.0, pocket_1
pseudoatom pocket_2, pos=[0.226, -6.273, 34.464], color=yellow
show spheres, pocket_2
set sphere_scale, 1.0, pocket_2
zoom
