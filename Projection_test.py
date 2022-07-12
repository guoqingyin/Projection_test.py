import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
import numpy as np
import cv2 as cv
# read in the intrinsics_depth and external_calibration from txt file
intrinsics_depth= np.zeros((4,4),dtype=float)
external_calibration= np.zeros((4,4),dtype=float)
f = open('D:\\IMAGINE\\scene0000_00\\stream\\intrinsics_depth.txt')
f1= open('D:\\IMAGINE\\scene0000_00\\stream\\pose\\004000.txt')
lines = f.readlines()
lines2= f1.readlines()
row = 0
list=[]
for line in lines:
    list = line.strip('\n').split(' ')
    intrinsics_depth[row:] = list[0:4]
    row+=1

row = 0
for line in lines2:
    list = line.strip('\n').split(' ')
    external_calibration[row:] = list[0:4]
    row+=1

# read the ply file
projection_matrix=np.dot(intrinsics_depth,external_calibration)[0:3,:]
pcd = o3d.io.read_point_cloud("D:\\IMAGINE\\scene0000_00\\scene0000_00_vh_clean_2.ply")
pcd_points=np.asarray(pcd.points)
pcd_color=np.asarray(pcd.colors)


one=np.ones((len(pcd_points),1))
pcd_points_concatenate=np.concatenate([pcd_points,one],axis=1)#each line have four valuers [x,y,z,1]

#(U,V,W).T=P*(x,y,z,1).T
pcd_points_projection=np.dot(projection_matrix,pcd_points_concatenate.T).T

#XI=U/W YI=V/W (XI,YI) means the coordinate in pixels
#!!!!!here, i always get the xi and yi in negative, I dont kown why
#so i add a negative sign in pcd_points_projection[:,2]
pcd_points_projection[:,0]=pcd_points_projection[:,0]/(-pcd_points_projection[:,2])
pcd_points_projection[:,1]=pcd_points_projection[:,1]/(-pcd_points_projection[:,2])
print(pcd_points_projection)
print(pcd_points_projection.shape)


pcd_save=[]
i=0
#U0,V0 from intrinsics_depth
width=638
height=485
for pcd_point in pcd_points_projection:

    if 0<pcd_point[1]<width and 0<pcd_point[0]<height :
        #I want to combine the coordinate in pixels with his color.
        #so the for each line of pcd_save have 5 values.[xi,yi,R,G,B]
        pcd_save.append([int(pcd_point[0]),int(pcd_point[1]),int(pcd_color[i][0]*256),int(pcd_color[i][1]*256),int(pcd_color[i][2]*256)])
    i+=1
pcd_save=np.asarray(pcd_save)
print(pcd_save.shape)
print(pcd_save)

#create a img with white background
img=np.zeros((height,width,3),np.uint8)
img[:,:,:]=[255,255,255]

for pcd_point in pcd_save:
    mycolor=[pcd_point[2],pcd_point[3],pcd_point[4]]
    img[pcd_point[0],pcd_point[1],:]=mycolor
    #the single pixel is too small to distinguish the color,
    #so i want pixel to be bigger like 3*3
    pacth_size=1
    for i in range(-pacth_size,pacth_size):
        for j in range(-pacth_size,pacth_size):
            x=pcd_point[0]+i
            y=pcd_point[1]+j
            if width>x>=0 and height>y>=0:
                img[x,y]=mycolor



cv.imshow("img",img)
cv.waitKey()
# pcd_points_projection=[pcd_points_projection[i] for i in range(2) ]
# print(pcd_points_projection)
 # PLOT THE IMAGE

