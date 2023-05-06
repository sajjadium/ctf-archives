import cv2
orig=cv2.imread("orig.bmp")
flag=cv2.imread("flag.bmp")
yoff,xoff=400,700
for i in range(flag.shape[0]):
    for j in range(flag.shape[1]):
        if flag[i][j][0]==0:
            assert(sum(orig[i+yoff][j+xoff]!=0)==3)
            orig[i+yoff][j+xoff][0]=0
            orig[i+yoff][j+xoff][1]=0
            orig[i+yoff][j+xoff][2]=0
cv2.imwrite("final.bmp",orig)