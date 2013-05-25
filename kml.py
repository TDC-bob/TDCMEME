#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     25/05/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import simplekml

def main():
    kml = simplekml.Kml()
    kml.newpoint(name="Kirstenbosch", coords=[(18.432314,-33.988862)])
    pnt = kml.newpoint(name="Icone de test", coords=[(18.432414,-33.988990)])
    pnt.iconstyle.icon.href = 'https://lh6.googleusercontent.com/-pyqo-LMmhos/AAAAAAAAAAI/AAAAAAAAAAA/WpBRYvZ7x4A/s27-c/photo.jpg'
    kml.save("botanicalgarden.kml")



if __name__ == '__main__':
    main()
