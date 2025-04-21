# PyMOL visualization script for predicted binding pockets
bg_color white
hide everything
show cartoon
color gray80
pseudoatom pocket_0, pos=[18.978, 18.583, 31.084], color=red
show spheres, pocket_0
set sphere_scale, 1.0, pocket_0
pseudoatom pocket_1, pos=[8.419, 11.240, -9.572], color=orange
show spheres, pocket_1
set sphere_scale, 1.0, pocket_1
pseudoatom pocket_2, pos=[18.994, 34.113, 25.198], color=yellow
show spheres, pocket_2
set sphere_scale, 1.0, pocket_2
pseudoatom pocket_3, pos=[4.648, 24.244, 3.269], color=green
show spheres, pocket_3
set sphere_scale, 1.0, pocket_3
zoom
