#encoding=utf-8
import exifread
import urllib2
import json
import shutil
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pyexiv2 as ev
import pygame
import StringIO
#from tkinter import *
import tkinter.font as tkFont  


class ImageHelper(object):
    def __init__(self):
        self.fpath = r'C:\Windows\Fonts\mingliu.ttc'
        # 26
        self.font = ImageFont.truetype(r'C:\Windows\Fonts\mingliu.ttc', 32)
        self.infile = 'D:\\temp\\test.bmp'
        self.outfile = 'D:\\temp\\test2.bmp'
        self.pngfile = 'D:\\temp\\test.png'
        pass

    def ImageToGray2(self,ifile,ofile):   
        im=Image.open(ifile)
        im2=im.convert("L")
        im2.save(ofile)
	
    def ImageToGray(self,ifile,ofile):
        with Image(filename=ifile,resolution=(300,300)) as img:
            img.type = 'grayscale'    
            img.save(filename=ofile)
        
    def ImageToTxt(self,ifile,ofile):
        image=Image.open(ifile)
        size=image.size
        pim = image.load()
        for i in range(size[1]):
         row='\n'
         for j in range(size[0]):
            if pim[j,i]==255:  #primb.putpixel((i,j), pima.getpixel((i,j)))   image.getpixel((5,5))
                row=row+'1 '
            else:
                row=row+str(pim[j,i])+' '
         with open(ofile,'a') as f:
                 f.write(row)
                 
    def ImageToBlank(self,ifile,ofile):
        image=Image.open(ifile)
        size=image.size
        nimage=Image.new('1', size)
        pim=image.load()
        npim=nimage.load()
        for i in range(size[0]):
            for j in range(size[1]):
                npim[i,j]=255   # "white"
        nimage.save(ofile)
    
    def GenImageByText4(self,text,fontsize,imgsize,outf):
        img0=Image.new('1',imgsize,"#FFFFFF")
        draw=ImageDraw.Draw(img0)
        font = ImageFont.truetype(self.fpath, fontsize)
        draw.text((0,0),text,font=font,fill=0)
        print font.getsize(text)
        img0.save(outf,dpi=(300,300))
        
    def GenImageByText3(self,text,fontsize,imgsize,outf):
        pygame.init()
        font = pygame.font.Font(self.fpath,fontsize)
        fsuface = font.render(text,True,(0,0,0))
        pygame.image.save(fsuface,self.pngfile)
        
    def GenImageByText2(self,text,fontsize,imgsize,outf):
        im = Image.new("RGB", imgsize, (255, 255, 255))
        pygame.init()
        font = pygame.font.Font(self.fpath,fontsize)
        font.set_bold(True)
        #render方法的第一个参数是写入的文字内容；第二个是布尔值，说明是否开启抗锯齿；第三个是字体本身的颜色；第四个是背景的颜色。如果不想有背景色，也就是让背景透明的话，可以不加第四个参数。
        rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
        #rtext = font.render(text, True,black)
        print font.size(text),font.get_bold(),font.get_height(),font.get_ascent(),font.get_descent()
        sio = StringIO.StringIO()
        pygame.image.save(rtext, sio)
        sio.seek(0)
        line = Image.open(sio)
        area = (0, 2)
        im.paste(line, area)
        #im.mode="1"
        #im.save(outf)
        im.save(self.pngfile,dpi=(640,640))

    def GenImageByText(self,text,size,outf):
        textsize =  self.font.getsize(text)
        im = Image.new("RGB", size, (255, 255, 255))
        dr = ImageDraw.Draw(im)
        w, h = dr.textsize(text, self.font)
        dr.text(textsize, text, font=self.font, fill="#000000")
        #print dr.textsize(text)
        im.save(outf)

    def PutTextOnImage(self,text,ifile,ofile):
        textsize =  self.font.getsize(text)
        im =Image.open(ifile)
        dr = ImageDraw.Draw(im)
        w, h = dr.textsize(text, self.font)
        dr.text((0,0), text, font=self.font, fill="#000000")
        im.save(ofile)

    def GetImageInfo(self,fpath):
        img=Image.open(fpath)
        size = img.size
        dpi = img.info.get('dpi')
        print "format:%s,size:%s pixels ,mode:%s,dpi:%s,compression:%s" % (img.format, str(img.size), img.mode, dpi, img.info.get('compression'))
        print "%s*%s inch" % (size[0]*1.0/dpi[0],size[1]*1.0/dpi[1])
        print "%s*%s cm" % (size[0]*2.54/dpi[0],size[1]*2.54/dpi[1])
        print "band:%s , box:%s" % (img.getbands(),img.getbbox())
        with open(fpath, 'rb') as f:
            tags = exifread.process_file(f)    
            if len(tags)>0:
                infostr = u"经度:%s,纬度:%s,照相机:%s,时间:%s" % (tags.get('GPS GPSLongitude'),tags.get('GPS GPSLatitude'),tags.get('Image Software'),tags.get('EXIF DateTimeOriginal'))
                print infostr
                # GPS
                print tags.get('GPS GPSLatitude'),tags.get('GPS GPSLongitude')
                wdu = self.ParseGps(str(tags.get('GPS GPSLatitude')).lstrip('[').rstrip(']'))
                jdu = self.ParseGps(str(tags.get('GPS GPSLongitude')).lstrip('[').rstrip(']'))
                print "wdu",wdu,"jdu",jdu
            
            for tag in tags.keys():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                    print "Key: %s, value %s" % (tag, tags[tag])


    def ParseGps(self,titude):
        first_number = titude.split(',')[0]
        second_number = titude.split(',')[1]
        third_number = titude.split(',')[2]
        third_number_parent = third_number.split('/')[0]
        third_number_child = third_number.split('/')[1]
        third_number_result = float(third_number_parent) / float(third_number_child)
        return float(first_number) + float(second_number)/60 + third_number_result/3600

    def fixed_size(self, width, height):
        """按照固定尺寸处理图片"""
        im = Image.open(self.infile)
        out = im.resize((width, height),Image.ANTIALIAS)
        out.save(self.outfile)

    def resize_by_width(self, w_divide_h):
        """按照宽度进行所需比例缩放"""
        im = Image.open(self.infile)
        (x, y) = im.size
        x_s = x
        y_s = x/w_divide_h
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(self.outfile)

    def resize_by_height(self, w_divide_h):
        """按照高度进行所需比例缩放"""
        im = Image.open(self.infile)
        (x, y) = im.size
        x_s = y*w_divide_h
        y_s = y
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(self.outfile)

    def resize_by_size(self, size):
        """按照生成图片文件大小进行处理(单位KB)"""
        size *= 1024
        im = Image.open(self.infile)
        size_tmp = os.path.getsize(self.infile)
        q = 100
        while size_tmp > size and q > 0:
            print q
            out = im.resize(im.size, Image.ANTIALIAS)
            out.save(self.outfile, quality=q)
            size_tmp = os.path.getsize(self.outfile)
            q -= 5
        if q == 100:
            shutil.copy(self.infile, self.outfile)

    def cut_by_ratio(self, width, height):
        """按照图片长宽比进行分割"""
        im = Image.open(self.infile)
        width = float(width)
        height = float(height)
        (x, y) = im.size
        if width > height:
            region = (0, int((y-(y * (height / width)))/2), x, int((y+(y * (height / width)))/2))
        elif width < height:
            region = (int((x-(x * (width / height)))/2), 0, int((x+(x * (width / height)))/2), y)
        else:
            region = (0, 0, x, y)

        #裁切图片
        crop_img = im.crop(region)
        #保存裁切后的图片
        crop_img.save(self.outfile)

    def to_deg(self,value, loc):
        """convert decimal coordinates into degrees, munutes and seconds tuple

        Keyword arguments: value is float gps-value, loc is direction list ["S", "N"] or ["W", "E"]
        return: tuple like (25, 13, 48.343 ,'N')
        """
        if value < 0:
            loc_value = loc[0]
        elif value > 0:
            loc_value = loc[1]
        else:
            loc_value = ""
        abs_value = abs(value)
        deg =  int(abs_value)
        t1 = (abs_value-deg)*60
        min = int(t1)
        sec = round((t1 - min)* 60, 5)
        return (deg, min, sec, loc_value)


    def set_gps_location(self,file_name, lat, lng):
        """Adds GPS position as EXIF metadata
        Keyword arguments:
        file_name -- image file
        lat -- latitude (as float)
        lng -- longitude (as float)

        """
        lat_deg = self.to_deg(lat, ["S", "N"])
        lng_deg = self.to_deg(lng, ["W", "E"])

        print lat_deg
        print lng_deg

        # class pyexiv2.utils.Rational(numerator, denominator) => convert decimal coordinates into degrees, munutes and seconds
        exiv_lat = (ev.Rational(lat_deg[0]*60+lat_deg[1],60),ev.Rational(lat_deg[2]*100,6000), ev.Rational(0, 1))
        exiv_lng = (ev.Rational(lng_deg[0]*60+lng_deg[1],60),ev.Rational(lng_deg[2]*100,6000), ev.Rational(0, 1))

        exiv_image = ev.ImageMetadata(file_name)
        exiv_image.read()

        # modify GPSInfo of image
        exiv_image["Exif.GPSInfo.GPSLatitude"] = exiv_lat
        exiv_image["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
        exiv_image["Exif.GPSInfo.GPSLongitude"] = exiv_lng
        exiv_image["Exif.GPSInfo.GPSLongitudeRef"] = lng_deg[3]
        exiv_image["Exif.Image.GPSTag"] = 654
        exiv_image["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
        exiv_image["Exif.GPSInfo.GPSVersionID"] = '2 2 0 0'
        exiv_image.write()


    
if __name__ == '__main__':
    text=u"元。"
    outf=r"d:\temp\3.bmp"
    im=ImageHelper()
    #生成文字图片
    fontsize = 32
    #im.GenImageByText4(text,fontsize,(76,40),r"d:\temp\test2.bmp")
    ofile = r"d:\temp\test.bmp"
    im.ImageToBlank(outf,ofile)
    im.PutTextOnImage(text,ofile,r"d:\temp\test2.bmp")
    '''
    #im.GetImageInfo(outf)
    print im.ConvertToAscii(outf,100)
    #im.cut_by_ratio(400,100)
    #把文字放图片上
    #im.PutTextOnImage(text)
    #修改GPS信息
    #im.set_gps_location(r"d:\temp\test2.jpg",22,113)
    '''
