@echo off
setlocal

set VENV_SCRIPTS=".\venv\Scripts\"

rem create virtual env
python -m venv venv

rem activate virtual env
call %VENV_SCRIPTS%activate.bat

rem install dependency package
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools

pip install numpy==1.18.0
pip install matplotlib==3.1.2
pip install requests==2.22.0
pip install beautifulsoup4==4.8.2

pip freeze

rem deactivate virtual env
call %VENV_SCRIPTS%deactivate.bat

pause

endlocal
