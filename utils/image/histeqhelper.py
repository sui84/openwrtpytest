# -*- coding: utf-8 -*-
from pylab import *
import copy
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def histeq2(ifile,ofile):
    # 读取图像到数组中
    im = array(Image.open(ifile))
    #获取通道
    r = im[:,:,0]
    g = im[:,:,1]
    b = im[:,:,2]
    #显示各个通道原始直方图，均值化之后的直方图以及累计分布函数
    figure()
    #计算各通道直方图
    imhist_r,bins_r = histogram(r,256,normed=True)
    imhist_g,bins_g = histogram(g,256,normed=True)
    imhist_b,bins_b = histogram(b,256,normed=True)
    subplot(331)
    hist(r.flatten(),256)
    subplot(332)
    hist(g.flatten(),256)
    subplot(333)
    hist(b.flatten(),256)

    #各通道累积分布函数
    cdf_r = imhist_r.cumsum()
    cdf_g = imhist_g.cumsum()
    cdf_b = imhist_b.cumsum()
    #累计函数归一化（由0～1变换至0~255）
    cdf_r = cdf_r*255/cdf_r[-1]
    cdf_g = cdf_g*255/cdf_g[-1]
    cdf_b = cdf_b*255/cdf_b[-1]
    #绘制累计分布函数
    subplot(334)
    plot(bins_r[:256],cdf_r)
    subplot(335)
    plot(bins_g[:256],cdf_g)
    subplot(336)
    plot(bins_b[:256],cdf_b)
    #绘制直方图均衡化之后的直方图
    im_r = interp(r.flatten(),bins_r[:256],cdf_r)
    im_g = interp(g.flatten(),bins_g[:256],cdf_g)
    im_b = interp(b.flatten(),bins_b[:256],cdf_b)

    # 显示直方图图像
    subplot(337)
    hist(im_r,256)
    subplot(338)
    hist(im_g,256)
    subplot(339)
    hist(im_b,256)
    #显示原始通道图与均衡化之后的通道图
    figure()
    gray()
    #原始通道图
    im_r_s = r.reshape([im.shape[0],im.shape[1]])
    im_g_s = g.reshape([im.shape[0],im.shape[1]])
    im_b_s = b.reshape([im.shape[0],im.shape[1]])

    #均衡化之后的通道图
    im_r = im_r.reshape([im.shape[0],im.shape[1]])
    im_g = im_g.reshape([im.shape[0],im.shape[1]])
    im_b = im_b.reshape([im.shape[0],im.shape[1]])
    subplot(231)
    imshow(im_r_s)
    subplot(232)
    imshow(im_g_s)
    subplot(233)
    imshow(im_b_s)

    subplot(234)
    imshow(im_r)
    subplot(235)
    imshow(im_g)
    subplot(236)
    imshow(im_b)
    #显示原始图像与均衡化之后的图像
    figure()
    #均衡化之后的图像
    im_p = copy.deepcopy(im)
    im_p[:,:,0] = im_r
    im_p[:,:,1] = im_g
    im_p[:,:,2] = im_b
    subplot(121)
    imshow(im)
    subplot(122)
    imshow(im_p)
    #show()
    imsave(ofile, im_p, format="png")
    #im_p.save(r"d:\temp\test.jpg")

def histeq1(ifile,ofile):
    #灰度图片
    from PIL import Image
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    image = Image.open(ifile).convert("L")
    image_array = np.array(image)
    plt.subplot(2,2,1)
    plt.hist(image_array.flatten(),256)
    plt.subplot(2,2,2)
    plt.imshow(image,cmap=cm.gray)
    plt.axis("off")
    plt.show()

    a = histeq(image_array)  # 利用刚定义的直方图均衡化函数对图像进行均衡化处理
    plt.subplot(2,2,3)
    plt.hist(a[0].flatten(),256)
    plt.subplot(2,2,4)
    nim=Image.fromarray(a[0])
    plt.imshow(nim,cmap=cm.gray)
    plt.axis("off")
    #plt.show()
    imsave(ofile, nim, format="png")


def histeq(image_array,image_bins=256):
    # 将图像矩阵转化成直方图数据，返回元组(频数，直方图区间坐标)
    image_array2,bins = np.histogram(image_array.flatten(),image_bins)

    # 计算直方图的累积函数
    cdf = image_array2.cumsum()

    # 将累积函数转化到区间[0,255]
    cdf = (255.0/cdf[-1])*cdf

    # 原图像矩阵利用累积函数进行转化，插值过程
    image2_array = np.interp(image_array.flatten(),bins[:-1],cdf)

    # 返回均衡化后的图像矩阵和累积函数
    return image2_array.reshape(image_array.shape),cdf


def show_hist2(ifile):
    from PIL import Image
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    #打开图像，并转化成灰度图像
    image = Image.open(ifile).convert("L")
    image_array = np.array(image)

    plt.subplot(2,1,1)
    plt.imshow(image,cmap=cm.gray)
    plt.axis("off")
    plt.subplot(2,1,2)
    plt.hist(image_array.flatten(),256) #flatten可以将矩阵转化成一维序列
    plt.show()

def show_hist(ifile):
    im = Image.open(ifile)
    im = im.convert('L')
    width, height = im.size
    pix = im.load()
    a = [0]*256
    for w in xrange(width):
        for h in xrange(height):
            p = pix[w,h]
            a[p] = a[p] + 1

    s = max(a)
    print a,len(a),s    #长度256,a保存的分别是颜色范围0-255出现的次数
    image = Image.new('RGB',(256,256),(255,255,255))
    draw = ImageDraw.Draw(image)

    for k in range(256):
        #print k,a[k],a[k]*200/s
        a[k] = a[k]*200/s       #映射范围0-200
        source = (k,255)        #起点坐标y=255, x=[0,1,2....]
        target = (k,255-a[k])   #终点坐标y=255-a[x],a[x]的最大数值是200,x=[0,1,2....]
        draw.line([source, target], (100,100,100))
    image.show()

def arrimage2(ifile,ofile):
    import matplotlib
    im=Image.open(ifile)
    imarr=np.array(im)
    matplotlib.image.imsave(ofile, imarr)

def arrimage(ifile,ofile):
    im=Image.open(ifile)
    imarr=np.array(im)
    im2=Image.fromarray(imarr)
    im2.save(ofile)

if __name__ == "__main__":
    arrimage2(r'd:\temp\1.jpg',r"d:\temp\test.png")
    #show_hist2(r'd:\temp\1.jpg')
    #histeq2(r"d:\temp\1.jpg",r"d:\temp\test.png")
