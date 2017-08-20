@echo off
SET pythonpath="%LocalAppData%\Programs\Python\Python36-32\python"
REM checking if python is installed
reg query "hkcu\software\Python" >nul 2>nul
if ERRORLEVEL 1 GOTO NOPYTHON
:PYDEPEND
%pythonpath% -c "import lxml" >nul 2>nul
if ERRORLEVEL 1 GOTO NOPYDEPEND
:PYSCRIPT
REM calling path validator script
%pythonpath% path_validator.py %*
pause
GOTO:EOF
:NOPYTHON
echo Python is not installed
echo Installing python ... please wait
python-3.6.2.exe /quiet PrependPath=1 >nul 2>nul
echo Python was installed successfully
GOTO PYDEPEND
:NOPYDEPEND
echo lxml is not installed
echo Installing lxml ... please wait
REM need to use this full path because batch does not refresh path variables
SET pippath="%LocalAppData%\Programs\Python\Python36-32\Scripts\pip.exe"
%pippath% install lxml >nul 2>nul
echo Lxml was installed successfully
GOTO PYSCRIPT