from pyexpat.errors import XML_ERROR_INCOMPLETE_PE
import sys
from collections import namedtuple
import numpy as np

K=1

PointTerrain = namedtuple('Point', 'x y z')
pointsTerrain = []
filenameTerrain = '../constant/triSurface/Mesh_Terrain.obj'

with open(filenameTerrain) as f:
    for line in f:
        line = line[:-1].split(' ')
        if line[0] == 'v':
            x, y, z = map(float, line[1:])
            pointsTerrain.append(PointTerrain(x, y, z))

lowest_point = min(pointsTerrain, key=lambda point: point.z)
minZ = lowest_point.z

PointBuildings = namedtuple('Point', 'x y z')
pointsBuildings = []
filenameBuildings = '../constant/triSurface/Mesh_Buildings.obj'

with open(filenameBuildings) as f:
    for line in f:
        line = line[:-1].split(' ')
        if line[0] == 'v':
            x, y, z = map(float, line[1:])
            pointsBuildings.append(PointBuildings(x, y, z))

# Coordinates from Terrain
minXdirection = min(pointsTerrain, key=lambda point: point.x)
minX = minXdirection.x
maxXdirection = max(pointsTerrain, key=lambda point: point.x)
maxX = maxXdirection.x
minYdirection = min(pointsTerrain, key=lambda point: point.y)
minY = minYdirection.y
maxYdirection = max(pointsTerrain, key=lambda point: point.y)
maxY = maxYdirection.y
minZdirection = min(pointsTerrain, key=lambda point: point.z)
centerXY = [minX+(maxX-minX)/2,minY+(maxY-minY)/2]

# Coordinates from Buildings
highest_point = max(pointsBuildings, key=lambda point: point.z)
H=highest_point.z
minXdirection = min(pointsBuildings, key=lambda point: point.x)
minXB = minXdirection.x
maxXdirection = max(pointsBuildings, key=lambda point: point.x)
maxXB = maxXdirection.x
minYdirection = min(pointsBuildings, key=lambda point: point.y)
minYB = minYdirection.y
maxYdirection = max(pointsBuildings, key=lambda point: point.y)
maxYB = maxYdirection.y
L=np.round(max(max(np.abs(maxXB-centerXY[0]),np.abs(maxYB-centerXY[1])),max(np.abs(minXB-centerXY[0]),np.abs(minYB-centerXY[1]))))

print("----------------- Terrain extension ------------------")
print("Xmin,Xmax = "+str(minX)+ ","+str(maxX))
print("Ymin,Ymax = "+str(minY)+ ","+str(maxY))
print("Zmin = "+str(minZ))
print("Terrain center: "+str(centerXY[0])+","+str(centerXY[1]))

print("----------------- Buildings extension ------------------")
print("Xmin,Xmax = "+str(minXB)+ ","+str(maxXB))
print("Ymin,Ymax = "+str(minYB)+ ","+str(maxYB))
print("Zmax = "+str(H))
print("Buildings maximum distance from Terrain center: "+str(L))

#boxlayers dimensions
xbl = [minX,maxX]
ybl = [minY,maxY]
zbl = [minZ,2]
print("----------------- Boxlayers ------------------")
print("Xmin,Xmax = "+str(xbl[0])+ ","+str(xbl[1]))
print("Ymin,Ymax = "+str(ybl[0])+ ","+str(ybl[1]))
print("Zmin,Zmax = "+str(zbl[0])+ ","+str(zbl[1]))
print("Boxlayers center: "+str(xbl[0]+(xbl[1]-xbl[0])/2)+","+str(ybl[0]+(ybl[1]-ybl[0])/2))
print("Boxlayers extension: "+str(xbl[1]-xbl[0])+","+str(ybl[1]-ybl[0])+","+str(zbl[1]))

#box0 dimensions
xb0 = [centerXY[0]-L-4*K*H,centerXY[0]+L+4*K*H]
yb0 = [centerXY[1]-L-4*K*H,centerXY[1]+L+4*K*H]
zb0 = [minZ,2*K*H]
print("----------------- Box0 ------------------")
print("Xmin,Xmax = "+str(xb0[0])+ ","+str(xb0[1]))
print("Ymin,Ymax = "+str(yb0[0])+ ","+str(yb0[1]))
print("Zmin,Zmax = "+str(zb0[0])+ ","+str(zb0[1]))
print("Box0 center: "+str(xb0[0]+(xb0[1]-xb0[0])/2)+","+str(yb0[0]+(yb0[1]-yb0[0])/2))
print("Box0 extension: "+str(xb0[1]-xb0[0])+","+str(yb0[1]-yb0[0])+","+str(zb0[1]))

#box1 dimensions
xb1 = [centerXY[0]-L-K*H,centerXY[0]+L+K*H]
yb1 = [centerXY[1]-L-K*H,centerXY[1]+L+K*H]
zb1 = [minZ,2*K*H]
print("----------------- Box1 ------------------")
print("Xmin,Xmax = "+str(xb1[0])+ ","+str(xb1[1]))
print("Ymin,Ymax = "+str(yb1[0])+ ","+str(yb1[1]))
print("Zmin,Zmax = "+str(zb1[0])+ ","+str(zb1[1]))
print("Box1 center: "+str(xb1[0]+(xb1[1]-xb1[0])/2)+","+str(yb1[0]+(yb1[1]-yb1[0])/2))
print("Box1 extension: "+str(xb1[1]-xb1[0])+","+str(yb1[1]-yb1[0])+","+str(zb1[1]))

#box2 dimensions
xb2 = [centerXY[0]-L/2-K*H,centerXY[0]+L/2+K*H]
yb2 = [centerXY[1]-L/2-K*H,centerXY[1]+L/2+K*H]
zb2 = [minZ,2*K*H]
print("----------------- Box2 ------------------")
print("Xmin,Xmax = "+str(xb2[0])+ ","+str(xb2[1]))
print("Ymin,Ymax = "+str(yb2[0])+ ","+str(yb2[1]))
print("Zmin,Zmax = "+str(zb2[0])+ ","+str(zb2[1]))
print("Box2 center: "+str(xb2[0]+(xb2[1]-xb2[0])/2)+","+str(yb2[0]+(yb2[1]-yb2[0])/2))
print("Box2 extension: "+str(xb2[1]-xb2[0])+","+str(yb2[1]-yb2[0])+","+str(zb2[1]))


# # // box 2
# # xb2_min #calc "$x_min - 4*$K*$z_max";
# # xb2_max #calc "$x_max + 4*$K*$z_max";
# # yb2_min #calc "$y_min - 4*$K*$z_max";
# # yb2_max #calc "$y_max + 12*$K*$z_max";
# # zb2_min $z_min;
# # zb2_max #calc "$z_max + 2*$K*$z_max";
