import pclpy
from pclpy import pcl
import open3d
import numpy as np
import math
f=open('result.txt',"r")
c=f.read().split('\n')
xyz,rgb=np.zeros((len(c)-1,3)),np.zeros((len(c)-1,3))
for i in range(len(c)-1):
    c[i]=c[i].split(' ')
    xyz[i][0],xyz[i][1],xyz[i][2]=float(c[i][0]),float(c[i][1]),float(c[i][2])
    rgb[i][0]=math.floor(min(255,float(c[i][3]))+0.5)
    rgb[i][1]=math.floor(min(255,float(c[i][4]))+0.5)
    rgb[i][2]=math.floor(min(255,float(c[i][5]))+0.5)
obj=pclpy.pcl.PointCloud.PointXYZRGB(xyz,rgb)
viewer = pcl.visualization.PCLVisualizer('PCD viewer')
viewer.addPointCloud(obj)
while(not viewer.wasStopped()):
    viewer.spinOnce(100)
pcl.io.savePLYFile("result.ply",obj)
pcl.io.loadPLYFile("src_4(1).ply",obj)
viewer = pcl.visualization.PCLVisualizer('PCD viewer')
viewer.addPointCloud(obj)
while(not viewer.wasStopped()):
    viewer.spinOnce(100)