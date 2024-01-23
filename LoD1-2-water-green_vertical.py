#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import griddata
import pyvista as pv

# SUBPLOTS FOR VELOCITY MAGNITUDE FOR THE 4 CASES

print('VELOCITY MAGNITUDE PLOTS') 
print(' ')

# sampled results from postProcessing > surfaces
surface_U1 = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD1/postProcessing/cuttingPlane/3002/U_xNormal.vtk')
surface_U2 = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD23/postProcessing/cuttingPlane/3002/U_xNormal.vtk')
surface_Uw = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD2wwater5/postProcessing/cuttingPlane/3002/U_xNormal.vtk')
surface_Uwg = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD2wwatergreen2/postProcessing/cuttingPlane/3002/U_xNormal.vtk')

# Clip any dataset by a set of XYZ bounds using the pyvista.DataSetFilters.clip_box() filter.
# clip part of domain (to only zoom in at study area for the results)
# terrain + buildings outline coordinates (copied from snappyHexMeshDict):
# bounding box LoD2 (-428.33 135.588 0) (439.98 881.833 97.9188)
x_min = -429
y_min = 136
z_min = 0
x_max = 440
y_max = 882
z_max = 200  # = H = H_terrain + H_maxbuilding = 2m + 118m
# bounds of clipping box specified as [xMin,xMax, yMin,yMax, zMin,zMax] of the 2 outer vertices:
bounds = [x_min-75,x_max+75, y_min-75,y_max+75, z_min, z_max]  # bounds of the box (the area you want to clip; rest will not be shown) 
clippedU1 = surface_U1.clip_box(bounds, invert=False)  # note: invert clip if you want to remove the box and keep everything around it 
clippedU2 = surface_U2.clip_box(bounds, invert=False)
clippedUw = surface_Uw.clip_box(bounds, invert=False)
clippedUwg = surface_Uwg.clip_box(bounds, invert=False)
U1_scalars = clippedU1.point_arrays['U']
U2_scalars = clippedU2.point_arrays['U']
Uw_scalars = clippedUw.point_arrays['U']
Uwg_scalars = clippedUwg.point_arrays['U']

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
    position_y=0.0,
    n_colors=40)
# _______________________________________________________________________________

# plotter set-up (create 4 subplots): LoD1, LoD2, LoD2 with water, LoD2 with water and vegetation
plotter = pv.Plotter(shape=(2, 2), border=False, window_size=(1000, 1000))
plotter.set_background("w")
pv.set_plot_theme("document")
# -------------
# LEFT TOP PLOT: LoD1 velocity
plotter.subplot(0, 0)
plotter.add_mesh(clippedU1, scalars=U1_scalars, clim=[-2,2], stitle='Velocity Magnitude [m/s]', scalar_bar_args=sargs, cmap="plasma_r") 
plotter.show_bounds(xlabel='',ylabel='y [m]',padding=0.9, font_size=16)
plotter.add_text('LoD1', font='courier', font_size=9, position=(230,420))
plotter.view_yz()
plotter.enable_zoom_style()
# -------------
# RIGHT TOP PLOT: LoD2 velocity
plotter.subplot(0, 1)
plotter.add_mesh(clippedU2, scalars=U2_scalars, clim=[-2,2], stitle='Velocity Magnitude [m/s]', scalar_bar_args=sargs, cmap="plasma_r")
plotter.show_bounds(xlabel='',ylabel='', font_size=16)
plotter.add_text('LoD2', font='courier', font_size=9, position=(230,420))
plotter.view_yz()
plotter.enable_zoom_style()
# -------------
# LEFT BOTTOM PLOT: LoD1 velocity
plotter.subplot(1, 0)
plotter.add_mesh(clippedUw, scalars=Uw_scalars, clim=[-2,2], stitle='Velocity Magnitude [m/s]', scalar_bar_args=sargs, cmap="plasma_r") 
plotter.show_bounds(xlabel='x [m]', ylabel='y [m]', font_size=16)
plotter.add_text('LoD2 with water', font='courier', font_size=9, position=(170,420))
plotter.view_yz()
plotter.enable_zoom_style()
# -------------
# RIGHT BOTTOM PLOT: LoD2 velocity
plotter.subplot(1, 1)
plotter.add_mesh(clippedUwg, scalars=Uwg_scalars, clim=[-2,2], stitle='Velocity Magnitude [m/s]', scalar_bar_args=sargs, cmap="plasma_r")
plotter.show_bounds(xlabel='x [m]',ylabel='', font_size=16)
plotter.add_text('LoD2 with water and vegetation', font='courier', font_size=9, position=(80,420))
plotter.view_yz()
plotter.enable_zoom_style()

# show and save the created subplots:
plotter.show(screenshot='/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/U_LoD1-2-water-green_vertical.png')