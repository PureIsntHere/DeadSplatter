@echo off
start %windir%\system32\rundll32.exe advapi32.dll,ProcessIdleTasks
exit /b
