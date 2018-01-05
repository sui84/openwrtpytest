#coding:utf-8
from images2gif import writeGif
import os
from PIL import Image

def split_gif(ifile,odir):
    f=Image.open(ifile)
    t=Image.new('P',f.size)
    p=f.getpalette()
    c=1
    try:
        while True:
            f.seek(f.tell()+1)
            t=f.copy()
            t.putpalette(p)
            t.save(os.path.join(odir,"test_%d.gif" % c),"gif")
            c+=1
    except EOFError:
        pass

def merge_gif(idir,ofile):
    li=os.listdir(idir)
    li.sort()
    iml=[]
    for key in li:
    #~ fp = open(di+key, "rb")
        img = Image.open(os.path.join(idir,key))
        iml.append(img)
    #~ size = (600,350)

    #~ for im in iml:
        #~ im.thumbnail(size, Image.ANTIALIAS)
    writeGif(ofile, iml, duration=0.05,nq=0.1)

if __name__ == "__main__":
    #split_gif(r"d:\temp\timg.gif",r"d:\temp\gif")
    '''Error:  File "E:\01_SOFT\Python27\lib\site-packages\images2gif\images2gif.py", line 347, in getSubRectangles
        im2 = im[y0:y1,x0:x1]
    TypeError: only integer scalar arrays can be converted to a scalar index
    '''
    merge_gif(r"d:\temp\gif",r"d:\temp\timg2.gif")
