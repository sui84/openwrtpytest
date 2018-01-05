<<<<<<< HEAD
import cv2
import numpy as np

def GenImageByText5(self,text,size,outf):
    '''
    w=500
    no_of_bits=8
    channels=3
    h=500
    image=cv.CreateImage((w,h),no_of_bits,channels)
    print image
    cv.SaveImage(outf,image)
    '''
    width, height = 300, 300
    image = np.zeros((height, width, 3), np.uint8)
    cv2.putText(image,'OpenCV',(10,500), self.font, 4,(255,255,255),2)
    cv2.imwrite(outf, image)
=======
# encoding=utf-8
import cv2
import numpy as np

def save_jpg(img,ofile,qua=100):
    cv2.imwrite(ofile,img,[int(cv2.IMWRITE_JPEG_QUALITY), qua])

def save_png(img,ofile,comp=0):
    cv2.imwrite(ofile, img, [int(cv2.IMWRITE_PNG_COMPRESSION), comp])

def show_img(imagePath):
    img = cv2.imread(imagePath)  #读取本地图片，目前OpevCV支持bmp、jpg、png、tiff
    cv2.namedWindow("Image")     #创建一个窗口用来显示图片
    cv2.imshow("Image", img)     #显示图片
    cv2.waitKey (0)              #等待输入,这里主要让图片持续显示。
    cv2.destroyAllWindows()      #释放窗口

def to_gray(img,ofile):
    eim=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    save_jpg(eim,ofile,100)

def add_image(ifile1,ifile2,ofile,weig1=0.7,weig2=0.3):
    img1 = cv2.imread(ifile1)
    img2 = cv2.imread(ifile2)
    dst = cv2.addWeighted(img1,weig1,img2,weig2,0)  # y设置为0
    save_jpg(dst,ofile)

def ontop_image(ifile1,ifile2):
    img1 = cv2.imread(ifile1)
    img2 = cv2.imread(ifile2)

    # 我想把logo放在左上脚，创建ROI
    rows,cols,channels = img2.shape
    roi = img1[0:rows, 0:cols ]

    # 创建logo的mask，和反mask
    img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    cv2.imshow('mask', mask)
    cv2.imshow('mask_inv', mask_inv)

    # 去掉ROI中的logo区域
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

    # 在opencv_logo图片中取logo
    img2_fg = cv2.bitwise_and(img2,img2,mask = mask)

    # 把图片放到ROI
    dst = cv2.add(img1_bg,img2_fg)
    # 修改lena.jpg图片
    img1[0:rows, 0:cols ] = dst

    cv2.imshow('res',img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def text_iamge(self,text,size,outf):
    '''
    w=500
    no_of_bits=8
    channels=3
    h=500
    image=cv.CreateImage((w,h),no_of_bits,channels)
    print image
    cv.SaveImage(outf,image)
    '''
    width, height = 300, 300
    image = np.zeros((height, width, 3), np.uint8)
    cv2.putText(image,'OpenCV',(10,500), self.font, 4,(255,255,255),2)
    cv2.imwrite(outf, image)

if __name__ == "__main__":
    #add_image(r'd:\temp\lena.png',r'd:\temp\chicky_512.png',r'd:\temp\test.jpg')
    ontop_image(r'd:\temp\lena.png',r'd:\temp\zj4.png')
>>>>>>> fa76b6b8c0c4837ccf695fb0c78faad35b770297
