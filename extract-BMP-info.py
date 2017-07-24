import struct
import sys
path=sys.argv[1]
with open(path,'rb') as file:
    try:
        read=file.read(30)
        bmp_info=struct.unpack('<ccIIIIIIHH',read)
        if bmp_info[0]==b'B' and (bmp_info[1]==b'M' or bmp_info[1]==b'A'):
            bmp_size=(bmp_info[6],bmp_info[7])
            bmp_color=bmp_info[9]
            print("图片大小为：%d * %d"%(bmp_size[0],bmp_size[1]))
            print("颜色数为：%d"%bmp_color)
        else:
            print("不是BMP位图")
    except :
        print("不是BMP位图")
