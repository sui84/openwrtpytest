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
