import open3d as o3d
import numpy as np
from matplotlib import pyplot as plt
from numpy import *

print("Load a ply point cloud, print it, and render it")
pcd = o3d.io.read_point_cloud("D:\\IMAGINE\\scene0000_00\\scene0000_00_vh_clean_2.ply")#读取ply点云数据
pcd_array=np.asarray(pcd.points)
pcd_color=np.asarray(pcd.colors)
print(pcd_array)#将pcd数据转化为numpy数组
print(pcd_color)
# print(pcd.colors[0])
# print(pcd_array.shape)
# print(pcd_color.shape)
o3d.visualization.draw_geometries([pcd])

#intrinsics_depth= zeros((4,4),dtype=float) #先创建一个 3x3的全零方阵A，并且数据的类型设置为float浮点型
# f = open('D:\\IMAGINE\\scene0000_00\\stream\\intrinsics_depth.txt') #打开数据文件文件
# lines = f.readlines() #把全部数据文件读到一个列表lines中
# row = 0 #表示矩阵的行，从0行开始
# list=[]
# for line in lines: #把lines中的数据逐行读取出来
#     list = line.strip('\n').split(' ') #处理逐行数据：strip表示把头尾的'\n'去掉，split表示以空格来分割行数据，然后把处理后的行数据返回到list列表中
#     intrinsics_depth[row:] = list[0:5] #把处理后的数据放到方阵A中。list[0:3]表示列表的0,1,2列数据放到矩阵A中的A_row行
#     row+=1 #然后方阵A的下一行接着读
# print(intrinsics_depth)