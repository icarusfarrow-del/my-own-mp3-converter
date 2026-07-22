@echo off
REM run.bat - Launches yt2mp3.py
REM Usage:
REM   run.bat <youtube-url> [output-directory]
REM   or just double-click and enter the URL when prompted

setlocal

REM Check that Python is available
where python >nul 2>nul
if errorlevel 1 (
    echo Error: Python is not installed or not on PATH.
    echo Download it from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check that yt-dlp is installed
python -c "import yt_dlp" >nul 2>nul
if errorlevel 1 (
    echo yt-dlp is not installed. Installing now...
    python -m pip install -U yt-dlp
)

REM Get the URL either from the argument or by prompting the user
set "URL=%~1"
if "%URL%"=="" (
    set /p URL="Enter YouTube URL: "
)

set "OUTDIR=%~2"

if "%OUTDIR%"=="" (
    python "%~dp0yt2mp3.py" "%URL%"
) else (
    python "%~dp0yt2mp3.py" "%URL%" "%OUTDIR%"
)

echo.
pause
