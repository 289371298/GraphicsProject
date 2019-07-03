#merge two point clouds created by meshlab into one
import pclpy
from pclpy import pcl
import open3d
import numpy as np
import math

def coloringWithDistance(x,y,z,a,b,obj):
    color=np.zeros(obj.xyz.shape)
    pos=np.array([x,y,z])
    for i in range(obj.xyz.shape[0]):
        if i%10000==0:print(i)
        #color[i]=np.matmul(A,(pos-obj.xyz[i]))
        color[i][0]=math.floor(math.fmod(a*abs(x-obj.xyz[i][0])+b,255))
        color[i][1]=math.floor(math.fmod(a*abs(y-obj.xyz[i][1])+b,255))
        color[i][2]=math.floor(math.fmod(a*abs(z-obj.xyz[i][2])+b,255))
    return pclpy.pcl.PointCloud.PointXYZRGB(obj.xyz,color.astype('uint8'))

obj,obj2=pclpy.pcl.PointCloud.PointXYZ(),pclpy.pcl.PointCloud.PointXYZ()
pcl.io.loadPLYFile("horsebody_alone.ply",obj)
pcl.io.loadPLYFile("dragonHead_alone.ply",obj2)#np.array([[1,0,2],[3,4,0],[2,1,2]]) np.array([[3,1,2],[4,0,1],[2,0,1]])
obj,obj2=coloringWithDistance(0,0,0,100,20,obj),coloringWithDistance(150,105,50,500,60,obj2)
obj3= pclpy.pcl.PointCloud.PointXYZRGB(np.r_[obj.xyz,obj2.xyz],np.r_[obj.rgb,obj2.rgb])
viewer = pcl.visualization.PCLVisualizer('PCD viewer')
viewer.addPointCloud(obj3)
while(not viewer.wasStopped()):
    viewer.spinOnce(100)
pcl.io.savePLYFile("test_on_629_night\\horsebody.ply",obj)
pcl.io.savePLYFile("test_on_629_night\\dragonHead.ply",obj2)