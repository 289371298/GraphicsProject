import pclpy
from pclpy import pcl
import open3d
import numpy as np
import math
obj, obj2 = pclpy.pcl.PointCloud.PointXYZRGB(), pclpy.pcl.PointCloud.PointXYZRGB()
pcl.io.loadPLYFile("src_4(1).ply",obj)#obj is src
pcl.io.loadPLYFile("tar_4(1).ply",obj2)#obj2 is tar
f=open("pt_src_4(1).txt","r")
c = f.read().split('\n')
KDT=pcl.search.KdTree.PointXYZRGB()
KDT.setInputCloud(obj2)
pos,dist,tag,List=pclpy.pcl.vectors.Int(),pclpy.pcl.vectors.Float(),np.zeros(obj.xyz.shape[0]),np.zeros(obj.xyz.shape[0])
for i in range(len(c)-1):
    c[i],tag[c[i]]=int(c[i]),1
    KDT.nearestKSearch(obj.points[c[i]], 1, pos, dist)
    List[c[i]]=int(pos[0])
    print(pos[0],dist[0])
obj3= pclpy.pcl.PointCloud.PointXYZRGB(np.r_[obj.xyz,obj2.xyz],np.r_[obj.rgb,obj2.rgb])
viewer = pcl.visualization.PCLVisualizer('PCD viewer')
viewer.addPointCloud(obj3)
while(not viewer.wasStopped()):
    viewer.spinOnce(100)
KDT2=pcl.search.KdTree.PointXYZRGB()
KDT2.setInputCloud(obj)
CONSTANT=10# important!!!
corre=[]
const=[]
for i in range(obj.xyz.shape[0]):
    if i%1000==0:print(i)
    if tag[i]:
        corre.append([i,i,1])
        const.append([obj2.r[int(List[i])],obj2.g[int(List[i])],obj2.b[int(List[i])],obj2.x[int(List[i])],obj2.y[int(List[i])],obj2.z[int(List[i])]])
        continue
    cnt,R,G,B,X,Y,Z=0,0,0,0,0,0,0
    KDT2.nearestKSearch(obj.points[i],CONSTANT,pos,dist)
    for j in range(len(pos)):
        #corre.append([i,pos[j],1])
        corre.append([i,pos[j],pow(math.e,-dist[j])])
        cnt=cnt+pow(math.e,-dist[j])
        R=R+pow(math.e,-dist[j])*obj.r[pos[j]]
        G=G+pow(math.e,-dist[j])*obj.g[pos[j]]
        B=B+pow(math.e,-dist[j])*obj.b[pos[j]]
        X=X+pow(math.e,-dist[j])*obj.x[pos[j]]
        Y=Y+pow(math.e,-dist[j])*obj.y[pos[j]]
        Z=Z+pow(math.e,-dist[j])*obj.z[pos[j]]
    #for j in range(len(pos)):
    corre.append([i,i,-cnt])
    const.append([R-cnt*obj.r[i], G-cnt*obj.g[i], B-cnt*obj.b[i], X-cnt*obj.x[i], Y-cnt*obj.y[i], Z-cnt*obj.z[i]])
print("len=",corre,const)
f=open("corre.txt","w")
for i in range(len(corre)):
    f.write(str(corre[i][0]+1)+" "+str(corre[i][1]+1)+" "+str(corre[i][2])+"\n")
g=open("const.txt","w")
for i in range(len(const)):
    for j in range(6):
        g.write(str(const[i][j])+" ")
    g.write("\n")