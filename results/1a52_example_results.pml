# PyMOL visualization script for predicted binding pockets
bg_color white
hide everything
show cartoon
color gray80
pseudoatom pocket_0, pos=[72.629, 20.856, 102.740], color=red
show spheres, pocket_0
set sphere_scale, 1.0, pocket_0
pseudoatom pocket_1, pos=[82.466, 35.954, 110.230], color=orange
show spheres, pocket_1
set sphere_scale, 1.0, pocket_1
zoom
