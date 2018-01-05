<<<<<<< HEAD
# -*- encoding=utf-8 -*-
import os
'''

    1 (1-bit pixels, black and white, stored with one pixel per byte)
    L (8-bit pixels, black and white)
    P (8-bit pixels, mapped to any other mode using a color palette)
    RGB (3x8-bit pixels, true color)
    RGBA (4x8-bit pixels, true color with transparency mask)
    CMYK (4x8-bit pixels, color separation)
    YCbCr (3x8-bit pixels, color video format)
    I (32-bit signed integer pixels)
    F (32-bit floating point pixels)
    
    im.resize((128, 128))                     #
    im.rotate(45)                             #逆时针旋转 45 度角。
    im.transpose(Image.FLIP_LEFT_RIGHT)       #左右对换。
    im.transpose(Image.FLIP_TOP_BOTTOM)       #上下对换。
    im.transpose(Image.ROTATE_90)             #旋转 90 度角。
    im.transpose(Image.ROTATE_180)            #旋转 180 度角。
    im.transpose(Image.ROTATE_270)            #旋转 270 度角。


    author: orangleliu
    pil处理图片，验证，处理
    大小，格式 过滤
    压缩，截图，转换

    图片库最好用Pillow
    还有一个测试图片test.jpg, 一个log图片，一个字体文件
    blend : 使用两幅给出的图片和一个常量 alpha 创建新的图片。两幅图片必须是同样的 size 和 mode 。
    Image.blend( image1, image2, alpha ) => image
    通过 list(im.getdata())  为其生成普通的序列。
    im.getpixel( xy ) => value or tuple 
    logoim.getpixel((1,1))
    histogram : 返回图像直方图，值为像素计数组成的列表
    img1 = img.copy()

    PIL.image.alpha_composite(im1,im2)
    PIL.image.blend(im1,im2,alpha)
    PIL.Image.composite(im1,im2,mask)
    这三个方法都属于图片的合成或者融合。都要求im1和im2的mode和size要一致，alpha代表图片占比的意思，而mask是mode可以为”1”,”L”或者”RGBA”的size和im1、im2一致的。

    绘制直线
    draw.line( ( (0,0), (width-1, height-1)), fill=255)
    绘制圆
    draw.arc( (0, 0, width-1, height-1), 0, 360, fill=255)
'''

#图片的基本参数获取
try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    import Image, ImageDraw, ImageFont, ImageEnhance


def trans_parency2(ifile,ofile,alpha=128):
    #half alpha
    img = Image.open(ifile)
    img.putalpha(128)
    img.save(ofile) 

def trans_parency(ifile,ofile, factor = 0.7 ):
    img = Image.open(ifile)
    img = img.convert('RGBA')  
    img_blender = Image.new('RGBA', img.size, (0,0,0,0))  
    img = Image.blend(img_blender, img, factor)  
    img.save(ofile) 

def image_enhance(ifile,factor=2.0):
    im=Image.open(ifile)
    #亮度增强
    brightness = ImageEnhance.Brightness(im)
    bright_img = brightness.enhance(factor)
    bright_img.show()
    #图像尖锐化
    sharpness = ImageEnhance.Sharpness(im)
    sharp_img = sharpness.enhance(factor)
    sharp_img.show()
    #对比度增强
    contrast = ImageEnhance.Contrast(im)
    contrast_img = contrast.enhance(factor)
    contrast_img.show()
    #色彩增强
    color = ImageEnhance.Color(im)
    color_img = color.enhance(factor)
    color_img.show()

def image_filter(ifile,ofile):
    '''
    # BLUR - 模糊处理
    # CONTOUR - 轮廓处理
    # DETAIL - 增强
    # EDGE_ENHANCE - 将图像的边缘描绘得更清楚
    # EDGE_ENHANCE_NORE - 程度比EDGE_ENHANCE更强
    # EMBOSS - 产生浮雕效果
    # SMOOTH - 效果与EDGE_ENHANCE相反，将轮廓柔和
    # SMOOTH_MORE - 更柔和
    # SHARPEN - 效果有点像DETAIL
    '''
    im = Image.open(ifile)
    im2=im.filter(ImageFilter.DETAIL)
    im2.save(ofile)

def trans_bg(ifile,ofile):
    img = Image.open(ifile)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = list()
    opacity_level = 0 #  0 完全透明 Opaque is 255, input between 0-255
    for item in datas:
        if item[0] >220 and item[1] > 220 and item[2] > 220:
            newData.append(( 255, 255, 255, opacity_level))
        else:
            newData.append(item)
    
    img.putdata(newData)
    img.save(ofile,"PNG")

    
def change_bgcolor(ifile,ofile):
    im = Image.open(ifile)
    x,y=im.size
    p=Image.new('RGBA',im.size,(67,142,219))   # (255,255,255)白底   (0,0,0) 黑底  (67,142,219)(0,191,243) 蓝底  (255,0,0)  红底
    p.paste(im,(0,0,x,y),im)
    p.save(ofile)
    
def merge_image(mode,files,ofile):
    # mode : RGB,RGBA,L,LA
    ims=[]
    for file in files:
        im=Image.open(file)
        ims.append(im)
    nim=Image.merge(mode,tuple(ims))
    nim.save(ofile)
        
def split_image(ifile):
    arr=Image.open(ifile).split()
    dirname = os.path.dirname(bg)
    for i in range(len(arr)):
        arr[i].save(os.path.join(dirname,"test"+str(i)+".jpg"))
    
def compress_image(img, w=128, h=128):
    '''
    缩略图
    '''
    img.thumbnail((w,h))
    im.save('test1.png', 'PNG')
    print u'成功保存为png格式, 压缩为128*128格式图片'

def cut_image(img):
    '''
    截图, 旋转，再粘贴
    '''
    #eft, upper, right, lower
    #x y z w  x,y 是起点， z,w是偏移值
    width, height = img.size
    box = (width-200, height-100, width, height)
    region = img.crop(box)
    #旋转角度
    region = region.transpose(Image.ROTATE_180)
    img.paste(region, box)
    img.save('test2.jpg', 'JPEG')
    print u'重新拼图成功'

def logo_watermark(img, logo_path,out_file):
    '''
    添加一个图片水印,原理就是合并图层，用png比较好
    新建的图片模式要选择RGBA模式newImg = Image.new('RGBA', (size*23, size))
    mask参数才可以保证png图片的半透明
    '''
    baseim = img
    logoim = Image.open(logo_path)
    bw, bh = baseim.size
    lw, lh = logoim.size
    baseim.paste(logoim, (bw-lw, bh-lh),mask=logoim)
    baseim.save(out_file, 'PNG')
    print u'logo水印组合成功'

def text_watermark(img, text, out_file=r"d:\temp\test4.jpg", angle=23, opacity=0.50):
    '''
    添加一个文字水印，做成透明水印的模样，应该是png图层合并
    http://www.pythoncentral.io/watermark-images-python-2x/
    这里会产生著名的 ImportError("The _imagingft C module is not installed") 错误
    Pillow通过安装来解决 pip install Pillow
    '''
    watermark = Image.new('RGBA', img.size, (255,255,255)) #我这里有一层白色的膜，去掉(255,255,255) 这个参数就好了

    FONT = "msyh.ttf"
    size = 2

    n_font = ImageFont.truetype(FONT, size)                                       #得到字体
    n_width, n_height = n_font.getsize(text)
    text_box = min(watermark.size[0], watermark.size[1])
    while (n_width+n_height <  text_box):
        size += 2
        n_font = ImageFont.truetype(FONT, size=size)
        n_width, n_height = n_font.getsize(text)                                   #文字逐渐放大，但是要小于图片的宽高最小值

    text_width = (watermark.size[0] - n_width) / 2
    text_height = (watermark.size[1] - n_height) / 2
    #watermark = watermark.resize((text_width,text_height), Image.ANTIALIAS)
    draw = ImageDraw.Draw(watermark, 'RGBA')                                       #在水印层加画笔
    draw.text((text_width,text_height),
              text, font=n_font, fill="#21ACDA")
    watermark = watermark.rotate(angle, Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(out_file, 'JPEG')
    print u"文字水印成功"


#等比例压缩图片
def resizeImg(ifile,ofile, dst_w=0, dst_h=0, qua=85):
    '''
    只给了宽或者高，或者两个都给了，然后取比例合适的
    如果图片比给要压缩的尺寸都要小，就不压缩了
    '''
    im = Image.open(ifile)
    ori_w, ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1

    if (ori_w and ori_w > dst_w) or (ori_h and ori_h  > dst_h):
        if dst_w and ori_w > dst_w:
            widthRatio = float(dst_w) / ori_w                                      #正确获取小数的方式
        if dst_h and ori_h > dst_h:
            heightRatio = float(dst_h) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio

        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h

    im.resize((newWidth,newHeight),Image.ANTIALIAS).save(ofile, "PNG", quality=qua)
    print u'等比压缩完成',ifile

    '''
    Image.ANTIALIAS还有如下值：
    NEAREST: use nearest neighbour
    BILINEAR: linear interpolation in a 2x2 environment
    BICUBIC:cubic spline interpolation in a 4x4 environment
    ANTIALIAS:best down-sizing filter
    '''
def resizeFolderImg(idir,odir, dst_w=0, dst_h=0, qua=85):
    files=os.listdir(idir)
    for f in files:
        ifile = os.path.join(idir,f)
        if os.path.isfile(ifile):
            ofile = os.path.join(odir,f)
            resizeImg(ifile,ofile, dst_w, qua)

#裁剪压缩图片
def clipResizeImg(im, dst_w, dst_h, qua=95):
    '''
        先按照一个比例对图片剪裁，然后在压缩到指定尺寸
        一个图片 16:5 ，压缩为 2:1 并且宽为200，就要先把图片裁剪成 10:5,然后在等比压缩
    '''
    ori_w,ori_h = im.size

    dst_scale = float(dst_w) / dst_h  #目标高宽比
    ori_scale = float(ori_w) / ori_h #原高宽比

    if ori_scale <= dst_scale:
        #过高
        width = ori_w
        height = int(width/dst_scale)

        x = 0
        y = (ori_h - height) / 2

    else:
        #过宽
        height = ori_h
        width = int(height*dst_scale)

        x = (ori_w - width) / 2
        y = 0

    #裁剪
    box = (x,y,width+x,height+y)
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None

    #压缩
    ratio = float(dst_w) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth,newHeight),Image.ANTIALIAS).save("test6.jpg", "JPEG",quality=95)
    print  "old size  %s  %s"%(ori_w, ori_h)
    print  "new size %s %s"%(newWidth, newHeight)
    print u"剪裁后等比压缩完成"


if __name__ == "__main__":
    #trans_parency(r'd:\temp\zj.jpg',r'd:\temp\zj3.png',factor=0.9)
    #trans_bg(r'd:\temp\zj.jpg',r'd:\temp\zj.png')
    #change_bgcolor(r'd:\temp\zj.png',r'd:\temp\zj2.png')
    #merge_image('RGB',[r"D:\Temp\test0.jpg",r"D:\Temp\test1.jpg",r"D:\Temp\test2.jpg"],r"d:\temp\test.jpg")
     #image 对象
    resizeImg(r'/mnt/sda1/temp/bq1.jpg',r'/mnt/sda1/temp/xl1.jpg', dst_w=200, qua=99)
    #resizeFolderImg(r'd:\temp\bq',r'd:\temp\bq\out', dst_w=200, qua=99)
    '''
    主要是实现功能， 代码没怎么整理
    '''
    '''
    im = Image.open('test.jpg')  #image 对象
    compress_image(im)

    im = Image.open('test.jpg')  #image 对象
    cut_image(im)

    im = Image.open(r'd:\temp\bg.png')  #image 对象
    logo_watermark(im, r'd:\temp\logo.png', r'd:\temp\test3.png')
    

    im = Image.open(r'd:\temp\test.jpg')  #image 对象
    text_watermark(im, 'Orangleliu', r'd:\temp\test3.png')
    


    im = Image.open('test.jpg')  #image 对象
    clipResizeImg(im, 100, 200)
    '''
=======
# -*- encoding=utf-8 -*-
import os
'''

    1 (1-bit pixels, black and white, stored with one pixel per byte)
    L (8-bit pixels, black and white)
    P (8-bit pixels, mapped to any other mode using a color palette)
    RGB (3x8-bit pixels, true color)
    RGBA (4x8-bit pixels, true color with transparency mask)
    CMYK (4x8-bit pixels, color separation)
    YCbCr (3x8-bit pixels, color video format)
    I (32-bit signed integer pixels)
    F (32-bit floating point pixels)
    
    im.resize((128, 128))                     #
    im.rotate(45)                             #逆时针旋转 45 度角。
    im.transpose(Image.FLIP_LEFT_RIGHT)       #左右对换。
    im.transpose(Image.FLIP_TOP_BOTTOM)       #上下对换。
    im.transpose(Image.ROTATE_90)             #旋转 90 度角。
    im.transpose(Image.ROTATE_180)            #旋转 180 度角。
    im.transpose(Image.ROTATE_270)            #旋转 270 度角。


    author: orangleliu
    pil处理图片，验证，处理
    大小，格式 过滤
    压缩，截图，转换

    图片库最好用Pillow
    还有一个测试图片test.jpg, 一个log图片，一个字体文件
    blend : 使用两幅给出的图片和一个常量 alpha 创建新的图片。两幅图片必须是同样的 size 和 mode 。
    Image.blend( image1, image2, alpha ) => image
    通过 list(im.getdata())  为其生成普通的序列。
    im.getpixel( xy ) => value or tuple 
    logoim.getpixel((1,1))
    histogram : 返回图像直方图，值为像素计数组成的列表
    img1 = img.copy()

    PIL.image.alpha_composite(im1,im2)
    PIL.image.blend(im1,im2,alpha)
    PIL.Image.composite(im1,im2,mask)
    这三个方法都属于图片的合成或者融合。都要求im1和im2的mode和size要一致，alpha代表图片占比的意思，而mask是mode可以为”1”,”L”或者”RGBA”的size和im1、im2一致的。

    绘制直线
    draw.line( ( (0,0), (width-1, height-1)), fill=255)
    绘制圆
    draw.arc( (0, 0, width-1, height-1), 0, 360, fill=255)
'''

#图片的基本参数获取
try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    import Image, ImageDraw, ImageFont, ImageEnhance


def trans_parency2(ifile,ofile,alpha=128):
    #half alpha
    img = Image.open(ifile)
    img.putalpha(128)
    img.save(ofile) 

def trans_parency(ifile,ofile, factor = 0.7 ):
    img = Image.open(ifile)
    img = img.convert('RGBA')  
    img_blender = Image.new('RGBA', img.size, (0,0,0,0))  
    img = Image.blend(img_blender, img, factor)  
    img.save(ofile) 

def image_enhance(ifile,factor=2.0):
    im=Image.open(ifile)
    #亮度增强
    brightness = ImageEnhance.Brightness(im)
    bright_img = brightness.enhance(factor)
    bright_img.show()
    #图像尖锐化
    sharpness = ImageEnhance.Sharpness(im)
    sharp_img = sharpness.enhance(factor)
    sharp_img.show()
    #对比度增强
    contrast = ImageEnhance.Contrast(im)
    contrast_img = contrast.enhance(factor)
    contrast_img.show()
    #色彩增强
    color = ImageEnhance.Color(im)
    color_img = color.enhance(factor)
    color_img.show()

def image_filter(ifile,ofile):
    '''
    # BLUR - 模糊处理
    # CONTOUR - 轮廓处理
    # DETAIL - 增强
    # EDGE_ENHANCE - 将图像的边缘描绘得更清楚
    # EDGE_ENHANCE_NORE - 程度比EDGE_ENHANCE更强
    # EMBOSS - 产生浮雕效果
    # SMOOTH - 效果与EDGE_ENHANCE相反，将轮廓柔和
    # SMOOTH_MORE - 更柔和
    # SHARPEN - 效果有点像DETAIL
    '''
    im = Image.open(ifile)
    im2=im.filter(ImageFilter.DETAIL)
    im2.save(ofile)

def trans_bg(ifile,ofile):
    img = Image.open(ifile)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = list()
    opacity_level = 0 #  0 完全透明 Opaque is 255, input between 0-255
    for item in datas:
        if item[0] >220 and item[1] > 220 and item[2] > 220:
            newData.append(( 255, 255, 255, opacity_level))
        else:
            newData.append(item)
    
    img.putdata(newData)
    img.save(ofile,"PNG")

    
def change_bgcolor(ifile,ofile):
    im = Image.open(ifile)
    x,y=im.size
    p=Image.new('RGBA',im.size,(67,142,219))   # (255,255,255)白底   (0,0,0) 黑底  (67,142,219)(0,191,243) 蓝底  (255,0,0)  红底
    p.paste(im,(0,0,x,y),im)
    p.save(ofile)
    
def merge_image(mode,files,ofile):
    # mode : RGB,RGBA,L,LA
    ims=[]
    for file in files:
        im=Image.open(file)
        ims.append(im)
    nim=Image.merge(mode,tuple(ims))
    nim.save(ofile)
        
def split_image(ifile):
    arr=Image.open(ifile).split()
    dirname = os.path.dirname(bg)
    for i in range(len(arr)):
        arr[i].save(os.path.join(dirname,"test"+str(i)+".jpg"))
    
def compress_image(img, w=128, h=128):
    '''
    缩略图
    '''
    img.thumbnail((w,h))
    im.save('test1.png', 'PNG')
    print u'成功保存为png格式, 压缩为128*128格式图片'

def cut_image(img):
    '''
    截图, 旋转，再粘贴
    '''
    #eft, upper, right, lower
    #x y z w  x,y 是起点， z,w是偏移值
    width, height = img.size
    box = (width-200, height-100, width, height)
    region = img.crop(box)
    #旋转角度
    region = region.transpose(Image.ROTATE_180)
    img.paste(region, box)
    img.save('test2.jpg', 'JPEG')
    print u'重新拼图成功'

def logo_watermark(img, logo_path,out_file):
    '''
    添加一个图片水印,原理就是合并图层，用png比较好
    新建的图片模式要选择RGBA模式newImg = Image.new('RGBA', (size*23, size))
    mask参数才可以保证png图片的半透明
    '''
    baseim = img
    logoim = Image.open(logo_path)
    bw, bh = baseim.size
    lw, lh = logoim.size
    baseim.paste(logoim, (bw-lw, bh-lh),mask=logoim)
    baseim.save(out_file, 'PNG')
    print u'logo水印组合成功'

def text_watermark(img, text, out_file=r"d:\temp\test4.jpg", angle=23, opacity=0.50):
    '''
    添加一个文字水印，做成透明水印的模样，应该是png图层合并
    http://www.pythoncentral.io/watermark-images-python-2x/
    这里会产生著名的 ImportError("The _imagingft C module is not installed") 错误
    Pillow通过安装来解决 pip install Pillow
    '''
    watermark = Image.new('RGBA', img.size, (255,255,255)) #我这里有一层白色的膜，去掉(255,255,255) 这个参数就好了

    FONT = "msyh.ttf"
    size = 2

    n_font = ImageFont.truetype(FONT, size)                                       #得到字体
    n_width, n_height = n_font.getsize(text)
    text_box = min(watermark.size[0], watermark.size[1])
    while (n_width+n_height <  text_box):
        size += 2
        n_font = ImageFont.truetype(FONT, size=size)
        n_width, n_height = n_font.getsize(text)                                   #文字逐渐放大，但是要小于图片的宽高最小值

    text_width = (watermark.size[0] - n_width) / 2
    text_height = (watermark.size[1] - n_height) / 2
    #watermark = watermark.resize((text_width,text_height), Image.ANTIALIAS)
    draw = ImageDraw.Draw(watermark, 'RGBA')                                       #在水印层加画笔
    draw.text((text_width,text_height),
              text, font=n_font, fill="#21ACDA")
    watermark = watermark.rotate(angle, Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(out_file, 'JPEG')
    print u"文字水印成功"


#等比例压缩图片
def resizeImg(ifile,ofile, dst_w=0, dst_h=0, qua=85):
    '''
    只给了宽或者高，或者两个都给了，然后取比例合适的
    如果图片比给要压缩的尺寸都要小，就不压缩了
    '''
    im = Image.open(ifile)
    ori_w, ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1

    if (ori_w and ori_w > dst_w) or (ori_h and ori_h  > dst_h):
        if dst_w and ori_w > dst_w:
            widthRatio = float(dst_w) / ori_w                                      #正确获取小数的方式
        if dst_h and ori_h > dst_h:
            heightRatio = float(dst_h) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio

        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h

    im.resize((newWidth,newHeight),Image.ANTIALIAS).save(ofile, "PNG", quality=qua)
    print u'等比压缩完成',ifile

    '''
    Image.ANTIALIAS还有如下值：
    NEAREST: use nearest neighbour
    BILINEAR: linear interpolation in a 2x2 environment
    BICUBIC:cubic spline interpolation in a 4x4 environment
    ANTIALIAS:best down-sizing filter
    '''
def resizeFolderImg(idir,odir, dst_w=0, dst_h=0,   qua=85):
    files=os.listdir(idir)
    for f in files:
        ifile = os.path.join(idir,f)
        if os.path.isfile(ifile):
            ofile = os.path.join(odir,f)
            resizeImg(ifile,ofile, dst_w,dst_h, qua)

#裁剪压缩图片
def clipResizeImg(im, dst_w, dst_h, qua=95):
    '''
        先按照一个比例对图片剪裁，然后在压缩到指定尺寸
        一个图片 16:5 ，压缩为 2:1 并且宽为200，就要先把图片裁剪成 10:5,然后在等比压缩
    '''
    ori_w,ori_h = im.size

    dst_scale = float(dst_w) / dst_h  #目标高宽比
    ori_scale = float(ori_w) / ori_h #原高宽比

    if ori_scale <= dst_scale:
        #过高
        width = ori_w
        height = int(width/dst_scale)

        x = 0
        y = (ori_h - height) / 2

    else:
        #过宽
        height = ori_h
        width = int(height*dst_scale)

        x = (ori_w - width) / 2
        y = 0

    #裁剪
    box = (x,y,width+x,height+y)
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None

    #压缩
    ratio = float(dst_w) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth,newHeight),Image.ANTIALIAS).save("test6.jpg", "JPEG",quality=95)
    print  "old size  %s  %s"%(ori_w, ori_h)
    print  "new size %s %s"%(newWidth, newHeight)
    print u"剪裁后等比压缩完成"


if __name__ == "__main__":
    #trans_parency(r'd:\temp\zj.jpg',r'd:\temp\zj3.png',factor=0.9)
    #trans_bg(r'd:\temp\zj.jpg',r'd:\temp\zj.png')
    #change_bgcolor(r'd:\temp\zj.png',r'd:\temp\zj2.png')
    #merge_image('RGB',[r"D:\Temp\test0.jpg",r"D:\Temp\test1.jpg",r"D:\Temp\test2.jpg"],r"d:\temp\test.jpg")
     #image 对象
    #resizeImg(r'd:\temp\bq1.jpg',r'd:\temp\xl1.jpg', dst_w=200, qua=99)
    resizeFolderImg(r'/usr/image/biaoqing',r'/usr/image/biaoqing/out', dst_w=200,dst_h= 0,qua=100)
    '''
    主要是实现功能， 代码没怎么整理
    '''
    '''
    im = Image.open('test.jpg')  #image 对象
    compress_image(im)

    im = Image.open('test.jpg')  #image 对象
    cut_image(im)

    im = Image.open(r'd:\temp\bg.png')  #image 对象
    logo_watermark(im, r'd:\temp\logo.png', r'd:\temp\test3.png')
    

    im = Image.open(r'd:\temp\test.jpg')  #image 对象
    text_watermark(im, 'Orangleliu', r'd:\temp\test3.png')
    


    im = Image.open('test.jpg')  #image 对象
    clipResizeImg(im, 100, 200)
    '''
>>>>>>> fa76b6b8c0c4837ccf695fb0c78faad35b770297
