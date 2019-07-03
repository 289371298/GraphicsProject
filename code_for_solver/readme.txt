代码运行要求：安装Python3.6（不能是3.7）及pclpy库。若pclpy安装后出现找不到dll的情况，则可能需要安装原pcl库。
1、coloror.py
    用于数据预处理，给无色点云上色：输入两个无色点云，输出并保存两个上色之后的结果。其中，coloringWithDistance函数接受x,y,z,a,b,obj六个参数，采用“每一维距固定点(x,y,z)的在这一维度上的距离，经过aX+b的线性变换后，对255取fmod再去尾”的方式给点云上色。
2、merger.py
    求解器的核心代码之一，接受两个点云和其中一个点云上手动选择的点的列表作为输入，在另一个点云上用KD树找到离它最近的点作为对应点。之后，以这些点作为边界条件构造矩阵和方程的常数项，并分别输出到corre.txt（系数）和const.txt（常数）。
3. graphicsolver.m
    求解器的核心代码之二，接受corre.txt和const.txt，以前者为矩阵、后者为常数项用gmres方法解线性方程组，并将结果输出到result.txt。每行六个数分别为Poisson编辑后点的XYZRGB。
4.checker.py
    验证答案，接受result.txt，并展示点云效果。

运行时，先运行merger.py，然后运行graphicsolver.m，最后运行checker.py。可以将产生的result.ply文件放进meshlab做进一步查看。