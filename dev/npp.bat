@echo off

REM This odd thing is needed to switch the drive to current directory.
set rootdir=%1
%rootdir:~1, +2%
cd %1 

C:\Python27\python.exe %2

REM This makes notepad++ work together with python. Let npp execute that command:
REM "npp.bat" "$(CURRENT_DIRECTORY)" "$(FILE_NAME)"

echo.
pause
