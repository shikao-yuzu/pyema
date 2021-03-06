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

pip install pytz==2019.3
pip install numpy==1.18.0
pip install pandas==0.25.3
pip install matplotlib==3.1.2
pip install japanize-matplotlib==1.0.5
pip install requests==2.22.0
pip install beautifulsoup4==4.8.2
pip install PyQt5==5.14.1

pip freeze

rem deactivate virtual env
call %VENV_SCRIPTS%deactivate.bat

pause

endlocal
