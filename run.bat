@echo off
setlocal

set VENV_SCRIPTS=".\venv\Scripts\"

if not exist %VENV_SCRIPTS%activate.bat (
  call create_venv.bat
)

rem activate virtual env
call %VENV_SCRIPTS%activate.bat

rem run
%VENV_SCRIPTS%python pyema\pyema.py

pause

rem deactivate virtual env
call %VENV_SCRIPTS%deactivate.bat

endlocal
