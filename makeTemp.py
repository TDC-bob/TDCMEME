#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     11/05/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import string, random, os


def random_string(prefix="", suffix="", size=8, chars=string.ascii_uppercase + string.digits):
   random_bit =  ''.join(random.choice(chars) for x in range(size))
##   return random_bit
   return "{}{}{}".format(prefix,random_bit,suffix)

def random_folder(base_path, prefix="", suffix="", size=8, chars=string.ascii_uppercase + string.digits):
    return os.path.join(base_path, random_string(prefix, suffix, size, chars))


def main():
    s1 = random_string()
    s2 = random_string("prefix")
    s3 = random_string(suffix="suffix")
    s4 = random_string(size=50)
    s5 = random_string(chars="ABCDE")
    print("\n".join([s1,s2,s3,s5]))
    f1 = random_folder(r"c:\windows", prefix="test_")
    print(f1)

if __name__ == '__main__':
    main()