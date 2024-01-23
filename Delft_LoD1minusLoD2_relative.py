#!/usr/bin/env python
# coding: utf-8

from imageio.core.request import URI_FILENAME
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from scipy.interpolate import griddata
import pyvista as pv


# # COMFORT MISMATCH PLOTS
# 

print('VELOCITY DIFFERENCE') 
print(' ')

U10 = 4.97 #velocity inflow 10 m height [m/s]
kappa =0.41
z0 = 0.5 # roughness length [m]
ustar = U10*kappa/(np.log((10+z0)/z0))
Uph = ustar/kappa*np.log((1.75+z0)/z0)

# sampled results from postProcessing > surfaces
surface_U1 = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD2/postProcessing/cuttingPlane/3002/U_zNormal.vtk')
surface_U2 = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD2wwater5/postProcessing/cuttingPlane/3002/U_zNormal.vtk')

# interpolation between the meshes for U:
U1_mesh1 = pv.PolyData(surface_U1)
U2_mesh2 = pv.PolyData(surface_U2)
U1_mesh2 = U2_mesh2.sample(U1_mesh1)

# Clip any dataset by a set of XYZ bounds using the pyvista.DataSetFilters.clip_box() filter.
# clip part of domain (to only zoom in at study area for the results)
# terrain + buildings outline coordinates (copied from snappyHexMeshDict):
# bounding box LoD2 (-428.33 135.588 0) (439.98 881.833 97.9188)
x_min = -429
y_min = 136
z_min = 0
x_max = 440
y_max = 882
z_max = 100  # = H = H_terrain + H_maxbuilding = 2m + 118m
# bounds of clipping box specified as [xMin,xMax, yMin,yMax, zMin,zMax] of the 2 outer vertices:
#bounds1 = [x_min-5,x_max+75, y_min-75,y_max, 3.84979009628, 3.84979009628]  # bounds of the box (the area you want to clip; rest will not be shown) 
bounds2 = [x_min-75,x_max+75, y_min-75,y_max+75, 3.70000004768, 3.70000004768]  # bounds of the box (the area you want to clip; rest will not be shown) 
#bounds2 = [x_min-75,x_max+75, y_min-75,y_max+75, 3.63599991798, 3.63599991798]  # bounds of the box (the area you want to clip; rest will not be shown) 
clippedU1 = U1_mesh2.clip_box(bounds2, invert=False)  # note: invert clip if you want to remove the box and keep everything around it 
clippedU2 = U2_mesh2.clip_box(bounds2, invert=False)

# take the norm of the velocity vector (magnitude):
clippedU1['magnitude'] = np.linalg.norm(clippedU1['U'], axis=1)
clippedU2['magnitude'] = np.linalg.norm(clippedU2['U'], axis=1)

# compute the difference
U_effect = ((clippedU2.point_arrays['magnitude'] - clippedU1.point_arrays['magnitude'])/Uph)*100
data_final_U = clippedU2
data_final_U.point_arrays['magnitude'] = U_effect 
deltaU_scalars = data_final_U.point_arrays['magnitude']

sargs = dict(
    color='k',
    font_family='courier',
    title_font_size=20,
    label_font_size=18,
    n_labels=10,
    fmt="%.1f",
    height=0.05, 
    width=0.5, 
    vertical=False, 
    position_x=0.75, 
    position_y=0.01,
    n_colors=20)

# _______________________________________________________________________________

# plotter set-up (create 2 subplots): bad pedestrian vs. good thermal comfort 
plotter = pv.Plotter(shape=(1, 1), border=False)
plotter.set_background("w")
pv.set_plot_theme("document")

# -------------
print(deltaU_scalars.min())
print(deltaU_scalars.max())

plotter.add_mesh(data_final_U, scalars=deltaU_scalars, clim=[-50,50], stitle='Relative Velocity Magnitude difference [%]', scalar_bar_args=sargs, cmap="plasma_r") 
plotter.show_bounds(xlabel='x [m]', ylabel='y [m]')
#plotter.add_text('VELOCITY LoD1', font='courier', font_size=9, position='upper_edge')
plotter.view_xy()   # plot the xy-plane
plotter.enable_zoom_style()   # enable to zoom in the image

# show and save the created subplots:
plotter.show(screenshot='/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/U1-U2_2mheight_relative_new.png')
