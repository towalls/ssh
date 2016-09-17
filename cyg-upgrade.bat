:: Released under the GNU General Public License version 3 by J2897.

@echo OFF
setlocal
title Cygwin Upgrader.
cls

:: Command-line parameters...
:: https://cygwin.com/faq/faq.html#faq.setup.cli
::
:: Add this to your .bashrc file...
:: alias cyg-upgrade="cygstart schtasks.exe /run /tn \"\Updates\Update Cygwin\""

REM Check for administrative privileges.
ver | find "Version 6." >nul
if %ERRORLEVEL% == 0 (
	openfiles >nul 2>&1
	if errorlevel 1 (
		msg %USERNAME% /time:600 Update aborted. You must run '%~nx0' as an administrator.
		exit /b 1
	)
)

REM Set the appropriate variables.
set "MIRROR=http://mirrors.kernel.org/sourceware/cygwin/"
set "CYGFILE32=setup-x86.exe"
set "CYGFILE64=setup-x86_64.exe"
set "LSF=%SYSTEMDRIVE%\cygstore"
set "UCS=%LSF%\scripts\update-cygwin-setup.py"

REM Find the Cygwin Setup File.
if exist "%LSF%\%CYGFILE64%" (set "FSF=%LSF%\%CYGFILE64%")
if exist "%LSF%\%CYGFILE32%" (set "FSF=%LSF%\%CYGFILE32%")

REM Upgrade Cygwin if the Folder and Setup File exists.
if not defined FSF (
	msg %USERNAME% /time:600 Update aborted. You may have deleted or renamed the Cygwin setup file.
	endlocal
	exit /b 1
)

REM Update the setup file if the Python script exists.
if exist "%SYSTEMDRIVE%\Python27\python.exe" (
	echo Attempting to update the setup file...
	"%SYSTEMDRIVE%\Python27\python.exe" "%UCS%" || echo Failed to update the setup file.
) else (
	echo Python 2.* isn't installed. So cannot check to see if the there's a newer
	echo setup file available. If there is, please put it in the 'cygstore' folder
	echo before your next auto-upgrade: %LSF%
)

echo.
echo Attempting to stop the sshd service...
net stop sshd

echo Killing processes...
taskkill /im "bash.exe" >nul 2>&1 || taskkill /im "bash.exe" /f >nul 2>&1
taskkill /im "sshd.exe" >nul 2>&1 || taskkill /im "sshd.exe" /f >nul 2>&1
echo.

echo Upgrading Cygwin packages...
if not exist "%USERPROFILE%\Logs" (md "%USERPROFILE%\Logs")
"%FSF%" -D -L -s "%MIRROR%" -q -g -o >"%USERPROFILE%\Logs\Cygwin Upgrade.log"

echo.
echo Attempting to start the sshd service...
net start sshd

:end
echo Ending . . .
endlocal
timeout /t 15 /nobreak >nul
exit /b 0
