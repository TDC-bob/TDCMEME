#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     23/05/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

# def res for briefing pictures: 512*512

def main():
    from PIL import Image
    im = Image.open(r"C:\Documents and Settings\owner\My Documents\BORIS\pics\prozac-dog1.jpg")
    w, h = im.size
    i = im.info
    f = im.format
    print("w: {}\th: {}\nformat: {}\ninfo: {}".format(w,h, f, i))
    im = im.resize((round(w/2),round(h/2)))
    im.rotate(45).show()

if __name__ == '__main__':
    main()
