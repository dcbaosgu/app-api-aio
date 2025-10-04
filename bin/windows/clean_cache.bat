@echo off
title Ultimate Ultra Pro Cleanup (Safe / Extreme)
color 0A
echo =========================================
echo     Ultimate Ultra Pro Cleanup Script
echo        Windows 10/11 - Safe / Extreme
echo =========================================
echo.

:: ---------------------------
:: Select mode
:CHOICE
set /p MODE=Choose mode (safe/extreme) [safe]: 
if /i "%MODE%"=="" set MODE=safe
if /i "%MODE%"=="safe" goto START
if /i "%MODE%"=="extreme" goto START
echo Invalid choice. Please type safe or extreme.
goto CHOICE

:START
echo Running in %MODE% mode...
echo.

:: ---------------------------
:: Identify the folders
set WIN_DIR=%windir%
set SYS_DRIVE=%systemdrive%
set USER_DIR=%userprofile%
set APPDATA_LOCAL=%USER_DIR%\AppData\Local
set APPDATA_ROAMING=%USER_DIR%\AppData\Roaming%
set PROGRAMDATA=%ProgramData%
set LOGFILE=%USER_DIR%\Desktop\cleanup_log.txt
echo Cleanup started at %date% %time% in %MODE% mode > "%LOGFILE%"

:: ---------------------------
:: 1. Clean temp and user cache (Safe & Extreme)
echo [*] Cleaning user temp, recent, cookies...
rd /s /q "%APPDATA_LOCAL%\Temp" 2>nul
md "%APPDATA_LOCAL%\Temp"
rd /s /q "%APPDATA_LOCAL%\Microsoft\Windows\INetCache" 2>nul
md "%APPDATA_LOCAL%\Microsoft\Windows\INetCache"
del /f /q "%APPDATA_LOCAL%\Microsoft\Windows\Cookies\*.*" 2>nul
del /f /q "%APPDATA_ROAMING%\Microsoft\Windows\Recent\*.*" 2>nul
echo User temp and caches cleaned >> "%LOGFILE%"

:: ---------------------------
:: 2. Clear browser cache (Safe & Extreme)
echo [*] Cleaning browser caches for all profiles...
:: Chrome
for /d %%i in ("%APPDATA_LOCAL%\Google\Chrome\User Data\*") do (
    rd /s /q "%%i\Cache" 2>nul
)
:: Edge
for /d %%i in ("%APPDATA_LOCAL%\Microsoft\Edge\User Data\*") do (
    rd /s /q "%%i\Cache" 2>nul
)
:: Firefox
for /d %%i in ("%APPDATA_ROAMING%\Mozilla\Firefox\Profiles\*") do (
    rd /s /q "%%i\cache2" 2>nul
)
echo Browser caches cleaned >> "%LOGFILE%"

:: ---------------------------
:: 3. Clean Windows Store & Thumbnail cache (Safe & Extreme)
echo [*] Cleaning Windows Store and Explorer thumbnail cache...
wsreset.exe >nul 2>&1
ie4uinit.exe -ClearIconCache >nul 2>&1
del /f /s /q "%LOCALAPPDATA%\Microsoft\Windows\Explorer\iconcache*" 2>nul
del /f /s /q "%LOCALAPPDATA%\Microsoft\Windows\Explorer\thumbcache*" 2>nul
echo Windows Store & thumbnail cache cleaned >> "%LOGFILE%"

:: ---------------------------
:: 4. Clean Recycle Bin (Safe & Extreme)
echo [*] Emptying Recycle Bin safely...
powershell -NoProfile -Command ^
"if (Test-Path 'C:\$Recycle.Bin') {Clear-RecycleBin -Force -ErrorAction SilentlyContinue}"
echo Recycle Bin emptied >> "%LOGFILE%"

:: ---------------------------
:: 5. Extreme Mode: Deeper Cleaning
if /i "%MODE%"=="extreme" (
    echo [*] Running Extreme cleanup...
    :: Clean all temp, logs, crash dumps, bak
    for %%e in (tmp log chk old gid dmp bak) do (
        del /f /s /q "%SYS_DRIVE%\*.%%e" 2>nul
    )
    :: Clean Windows temp, prefetch, logs hệ thống, Explorer thumbnail cache
    rd /s /q %WIN_DIR%\Temp 2>nul
    md %WIN_DIR%\Temp
    del /f /s /q %WIN_DIR%\Prefetch\*.* 2>nul
    del /f /s /q %WIN_DIR%\Logs\*.* 2>nul
    del /f /s /q %WIN_DIR%\System32\winevt\Logs\*.* 2>nul
    del /f /s /q "%APPDATA_LOCAL%\Microsoft\Windows\Explorer\thumbcache*.*" 2>nul
    :: Clean temp/cache mọi ứng dụng (AppData + ProgramData)
    for /d %%i in ("%APPDATA_LOCAL%\*") do (
        if exist "%%i\Temp" rd /s /q "%%i\Temp" 2>nul
        if exist "%%i\Cache" rd /s /q "%%i\Cache" 2>nul
    )
    for /d %%i in ("%APPDATA_ROAMING%\*") do (
        if exist "%%i\Temp" rd /s /q "%%i\Temp" 2>nul
        if exist "%%i\Cache" rd /s /q "%%i\Cache" 2>nul
    )
    for /d %%i in ("%PROGRAMDATA%\*") do (
        if exist "%%i\Temp" rd /s /q "%%i\Temp" 2>nul
        if exist "%%i\Cache" rd /s /q "%%i\Cache" 2>nul
    )
    echo Extreme cleanup completed >> "%LOGFILE%"
)

:: ---------------------------
:: 6. Completed
echo.
echo =========================================
echo Cleanup completed successfully in %MODE% mode!
echo See log on Desktop: cleanup_log.txt
echo =========================================
pause
