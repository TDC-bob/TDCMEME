@echo off
set /p msg="Enter message: " %=%
git add *
git commit -a -m "%msg%" && git push
pause