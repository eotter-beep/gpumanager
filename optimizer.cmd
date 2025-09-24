DISM /Online /Cleanup-Image /ScanHealth
REM Get the GUID for the "Power saver" scheme
for /f "tokens=3" %%A in ('powercfg /list ^| findstr /i "Power saver"') do set guid=%%A

REM Set the Power saver scheme as active
powercfg /setactive %guid%

echo Power Saver mode activated!
%windir%\system32\rundll32.exe advapi32.dll,ProcessIdleTasks
