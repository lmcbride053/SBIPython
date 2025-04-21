# PyMOL visualization script for predicted binding pockets
bg_color white
hide everything
show cartoon
color gray80
pseudoatom pocket_0, pos=[-36.093, -1.035, 23.734], color=red
show spheres, pocket_0
set sphere_scale, 1.0, pocket_0
pseudoatom pocket_1, pos=[-41.640, 61.951, 38.547], color=orange
show spheres, pocket_1
set sphere_scale, 1.0, pocket_1
zoom
