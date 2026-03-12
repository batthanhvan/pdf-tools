@echo off
setlocal enabledelayedexpansion
echo.
echo.

set DPI=300
set ALPHABITS=2
set QUALITY=80
set FIRSTPAGE=1
set LASTPAGE=9999
REM MEMORY in MB
set MEMORY=300

set "GS=%~1"
IF "%GS%" == "" set "GS=bin\gswin32c.exe"
shift /1

echo Loading %GS%...
echo.

REM Process each file passed as parameter (supports drag & drop of multiple PDFs)
:loop
if "%~1"=="" goto done
if /I not "%~x1"==".pdf" (
	shift /1
	goto loop
)
pushd "%~dp1" || (
	echo The system cannot find the path specified: "%~dp1"
	shift /1
	goto loop
)
set "PDFFILE=%~nx1"
set "JPGFILE=!PDFFILE:.pdf=-%%d.jpg!"

echo Converting: !PDFFILE!

"%~dp0%GS%" -sDEVICE=jpeg -sOutputFile="!JPGFILE!" -r%DPI% -dNOPAUSE -dFirstPage=%FIRSTPAGE% -dLastPage=%LASTPAGE% -dJPEGQ=%QUALITY% -dGraphicsAlphaBits=%ALPHABITS%  -dTextAlphaBits=%ALPHABITS%  -dNumRenderingThreads=4 -dBufferSpace=%MEMORY%000000  -dBandBufferSpace=%MEMORY%000000 -c %MEMORY%000000 setvmthreshold -f "!PDFFILE!" -c quit
popd
shift /1
goto loop

:done

echo Finished.
pause
endlocal
