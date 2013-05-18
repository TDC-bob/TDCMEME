# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Author:      Bob Daribouca
#
# Copyright:   (c) Bob Daribouca 2013
# Licence:     CC BY-NC-SA 3.0
#
#               Please refer to the "LICENSE" file distributed with the package,
#               or to http://creativecommons.org/licenses/by-nc-sa/3.0/
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from distutils.core import setup

##setup(name='Distutils',
##      version='1.0',
##      description='Python Distribution Utilities',
##      author='Greg Ward',
##      author_email='gward@python.net',
##      url='http://www.python.org/sigs/distutils-sig/',
##      packages=['distutils', 'distutils.command'],
##     )


setup(name='tdcmeme',
      version='0.0.1',
      author='bob Daribouca',
      license='CC BY-NC-SA 3.0',
      copyright='Bob Daribouca',
      py_modules=['_logging','_slpp','Exceptions','main','makeTemp','mission','mizFile','tests'],
      packages=['campaign'],
      data_files=[('slpp tests', ['slpp tests/mission'])]



      )
