#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from scipy.interpolate import griddata
import pyvista as pv


# # COMFORT MISMATCH PLOTS
# 

print('VELOCITY MISMATCH') 
print(' ')

# sampled results from postProcessing > surfaces
surface_U1 = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD1/postProcessing/cuttingPlane/3002/U_zNormal.vtk')
surface_U2 = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD23/postProcessing/cuttingPlane/3002/U_zNormal.vtk')

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
bounds1 = [x_min-75,x_max+75, y_min-75,y_max+75, 3.70000004768, 3.70000004768]  # bounds of the box (the area you want to clip; rest will not be shown) 
bounds2 = [x_min-75,x_max+75, y_min-75,y_max+75, 3.70000004768, 3.70000004768]  # bounds of the box (the area you want to clip; rest will not be shown) 
clippedU1 = surface_U1.clip_box(bounds1, invert=False)  # note: invert clip if you want to remove the box and keep everything around it 
clippedU2 = surface_U2.clip_box(bounds2, invert=False)
U1_scalars = clippedU1.point_arrays['U']
U2_scalars = clippedU2.point_arrays['U']

sargs = dict(
    color='k',
    font_family='courier',
    title_font_size=20,
    label_font_size=18,
    n_labels=10,
    fmt="%.1f",
    height=0.05, 
    width=0.8, 
    vertical=False, 
    position_x=0.9, 
    position_y=0.05,
    n_colors=20)

# _______________________________________________________________________________

# plotter set-up (create 2 subplots): bad pedestrian vs. good thermal comfort 
plotter = pv.Plotter(shape=(1, 2), border=False)
plotter.set_background("w")
pv.set_plot_theme("document")

# -------------

# LEFT PLOT: LoD1 velocity
plotter.subplot(0, 0)

plotter.add_mesh(clippedU1, scalars=U1_scalars, clim=[0,4.9], stitle='Velocity Magnitude [m/s]', scalar_bar_args=sargs, cmap="plasma_r") 
plotter.show_bounds(xlabel='x [m]', ylabel='y [m]')
plotter.add_text('VELOCITY LoD1', font='courier', font_size=9, position=(190,120))
plotter.view_xy()   # plot the xy-plane
plotter.enable_zoom_style()   # enable to zoom in the image

# -------------

# RIGHT PLOT: LoD2 velocity
plotter.subplot(0, 1)

plotter.add_mesh(clippedU2, scalars=U2_scalars, clim=[0,4.9], stitle='Velocity Magnitude [m/s]', scalar_bar_args=sargs, cmap="plasma_r")
plotter.show_bounds(xlabel='x [m]', ylabel='y [m]')
plotter.add_text('VELOCITY LoD2', font='courier', font_size=9, position=(190,120))
plotter.view_xy()   # plot the xy-plane
plotter.enable_zoom_style()   # enable to zoom in the image

# show and save the created subplots:
plotter.show(screenshot='/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/U1andU2_2mheight_new.png')
