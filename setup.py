from distutils.core import setup
setup(name='tdcmeme',
      version='0.0.1',
      author='Bob Daribouca',
      license='CC BY-NC-SA 3.0',
      copyright='Bob Daribouca',
      py_modules=['_slpp','Exceptions','main','makeTemp','mission','mizfile'],
      packages=['campaign','_logging','tests'],
      data_files=[('tests/slpp_tests', ['Travis/MiG-29S - Abkhaz Fulcrums.miz'])]
      )