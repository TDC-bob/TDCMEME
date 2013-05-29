@echo off
nosetests --no-skip --verbosity=2 --with-coverage --cover-erase --cover-html --cover-html-dir="C:\Documents and Settings\owner\My Documents\BORIS\TDC\TDCMEME.pages" --debug-log=nose-run.log --logging-level=INFO --detailed-errors 
REM --cover-package=missions --cover-package=_logging --cover-package=bobgit --cover-package=campaign
pause