#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import griddata
import pyvista as pv

# SUBPLOTS FOR VELOCITY MAGNITUDE RELATIVE DIFFERENCE WITH LOD2

print('VELOCITY MAGNITUDE DIFFERENCES') 
print(' ')

# general data to make plots relative with respect to the inflow velocity at the same height
U10 = 4.97 #velocity inflow 10 m height [m/s]
kappa =0.41
z0 = 0.5 # roughness length [m]
ustar = U10*kappa/(np.log((10+z0)/z0))
Uph = ustar/kappa*np.log((1.75+z0)/z0)

# sampled results from postProcessing > surfaces
surface_U1 = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD1/postProcessing/cuttingPlane/3002/U_zNormal.vtk')
surface_U2 = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD23/postProcessing/cuttingPlane/3002/U_zNormal.vtk')
surface_Uw = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD2wwater5/postProcessing/cuttingPlane/3002/U_zNormal.vtk')
surface_Uwg = pv.read('/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/LoD2wwatergreen2/postProcessing/cuttingPlane/3002/U_zNormal.vtk')

# interpolation between the meshes for U:
U1_mesh1 = pv.PolyData(surface_U1)
U2_mesh2 = pv.PolyData(surface_U2)
Uw_meshw = pv.PolyData(surface_Uw)
Uwg_meshwg = pv.PolyData(surface_Uwg)
U1_mesh2 = U2_mesh2.sample(U1_mesh1)
U2_mesh2 = pv.PolyData(surface_U2)
Uw_mesh2 = U2_mesh2.sample(Uw_meshw)
U2_mesh2 = pv.PolyData(surface_U2)
Uwg_mesh2 = U2_mesh2.sample(Uwg_meshwg)

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
bounds = [x_min-75,x_max+75, y_min-75,y_max+75, 3.70000004768, 3.70000004768]  # bounds of the box (the area you want to clip; rest will not be shown) 
clippedU1 = U1_mesh2.clip_box(bounds, invert=False)  # note: invert clip if you want to remove the box and keep everything around it 
clippedU2 = U2_mesh2.clip_box(bounds, invert=False)
clippedUw = Uw_mesh2.clip_box(bounds, invert=False)
clippedUwg = Uwg_mesh2.clip_box(bounds, invert=False)

# take the norm of the velocity vector (magnitude):
clippedU1['magnitude'] = np.linalg.norm(clippedU1['U'], axis=1)
clippedU2['magnitude'] = np.linalg.norm(clippedU2['U'], axis=1)
clippedUw['magnitude'] = np.linalg.norm(clippedUw['U'], axis=1)
clippedUwg['magnitude'] = np.linalg.norm(clippedUwg['U'], axis=1)

# compute the difference
U21_effect = ((clippedU2.point_arrays['magnitude'] - clippedU1.point_arrays['magnitude'])/Uph)*100
U2w_effect = ((clippedU2.point_arrays['magnitude'] - clippedUw.point_arrays['magnitude'])/Uph)*100
U2wg_effect = ((clippedU2.point_arrays['magnitude'] - clippedUwg.point_arrays['magnitude'])/Uph)*100

data_final_U21 = clippedU2.copy()
data_final_U21.point_arrays['magnitude'] = U21_effect 
deltaU21_scalars = data_final_U21.point_arrays['magnitude']
data_final_U2w = clippedU2.copy()
data_final_U2w.point_arrays['magnitude'] = U2w_effect 
deltaU2w_scalars = data_final_U2w.point_arrays['magnitude']
data_final_U2wg = clippedU2.copy()
data_final_U2wg.point_arrays['magnitude'] = U2wg_effect 
deltaU2wg_scalars = data_final_U2wg.point_arrays['magnitude']

sargs = dict(
    color='k',
    font_family='courier',
    title_font_size=18,
    label_font_size=16,
    n_labels=9,
    fmt="%.1f",
    height=0.1, 
    width=0.8, 
    vertical=False, 
    position_x=0.9, 
    position_y=0.87,
    n_colors=40)
# _______________________________________________________________________________

# plotter set-up (create 4 subplots): LoD1, LoD2, LoD2 with water, LoD2 with water and vegetation
plotter = pv.Plotter(shape=(3, 1), border=False, window_size=(500, 1400))
plotter.set_background("w")
pv.set_plot_theme("document")
# -------------
# LEFT PLOT: (LoD2-LoD1)/inflow same height velocity
print(deltaU21_scalars.min())
print(deltaU21_scalars.max())
plotter.subplot(0, 0)
plotter.add_mesh(data_final_U21, scalars=deltaU21_scalars, clim=[-50,50], stitle='Velocity Difference [%]', scalar_bar_args=sargs, cmap="plasma_r") 
plotter.show_bounds(xlabel='x [m]',ylabel='y [m]', font_size=16)
plotter.add_text('LoD2.2-LoD1.3', font='courier', font_size=9, position=(185,380))
plotter.view_xy()
plotter.enable_zoom_style()
# -------------
# CENTER PLOT: (LoD2-LoD2w)/inflow same height velocity
print(deltaU2w_scalars.min())
print(deltaU2w_scalars.max())
plotter.subplot(1, 0)
plotter.add_mesh(data_final_U2w, scalars=deltaU2w_scalars, clim=[-50,50], scalar_bar_args=sargs, cmap="plasma_r") 
plotter.show_bounds(xlabel='x [m]',ylabel='y [m]', font_size=16)
plotter.add_text('LoD2.2 - LoD2.2 with water', font='courier', font_size=9, position=(110,380))
plotter.view_xy()
plotter.enable_zoom_style()
# -------------
# RIGHT PLOT: (LoD2-LoD2wg)/inflow same height velocity
print(deltaU2wg_scalars.min())
print(deltaU2wg_scalars.max())
plotter.subplot(2, 0)
plotter.add_mesh(data_final_U2wg, scalars=deltaU2wg_scalars, clim=[-50,50], scalar_bar_args=sargs, cmap="plasma_r") 
plotter.show_bounds(xlabel='x [m]', ylabel='y [m]', font_size=16)
plotter.add_text('LoD2.2 - LoD2.2 with water and vegetation', font='courier', font_size=9, position=(30,380))
plotter.view_xy()
plotter.enable_zoom_style()

# show and save the created subplots:
plotter.show(screenshot='/Users/claragarciasan/Documents/TUD/Research/DelftProject/LoDs/simulations/reducedMesh/U_LoD1-2-water-green_pedestrianheight_relativedifference.png')