@echo off
C:\Python33\Scripts\nosetests --no-skip --verbosity=2 --with-coverage --cover-erase --cover-html --cover-html-dir="..\TDCMEME.pages" --debug-log=nose-run.log --logging-level=INFO --detailed-errors
REM --cover-package=missions --cover-package=_logging --cover-package=bobgit --cover-package=campaign
pause