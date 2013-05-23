@echo off
rmdir /S /Q COVER
nosetests --no-skip --verbosity=2 --with-coverage --cover-erase --cover-html --cover-html-dir=COVER --debug-log=nose-run.log --logging-level=INFO --detailed-errors
pause