@echo off
setlocal enabledelayedexpansion
echo.
echo.

REM Ghostscript paths to try - 64-bit first, then 32-bit
set "GS64=%~dp0bin\gswin64c.exe"
set "GS32=%~dp0bin\gswin32c.exe"
set "GS_PATH="

REM Try to find Ghostscript installation
if exist "%GS64%" (
    set "GS_PATH=%GS64%"
    echo Using Ghostscript 64-bit
) else if exist "%GS32%" (
    set "GS_PATH=%GS32%"
    echo Using Ghostscript 32-bit
) else (
    echo.
    echo ERROR: Ghostscript not found!
    echo.
    echo Please download and install Ghostscript from:
    echo http://www.ghostscript.com/download/gsdnld.html
    echo.
    echo After installation, open this file in Notepad and update the GS64 and GS32 
    echo paths to match your Ghostscript installation directory.
    echo.
    pause
    exit /b 1
)

echo.

REM Check if any PDF files were provided
if "%~1"=="" (
    echo Usage: Drag and drop PDF files onto this batch file.
    echo.
    echo Example: combine-pdf.bat table_1.pdf table_2.pdf table_3.pdf
    echo.
    pause
    exit /b 1
)

REM Count PDF files and collect them
set "PDF_LIST="
set "PDF_COUNT=0"

for %%A in (%*) do (
    if /I "%%~xA"==".pdf" (
        set /A PDF_COUNT+=1
        set "PDF_LIST=!PDF_LIST! "%%~fA""
    )
)

if %PDF_COUNT% LSS 2 (
    echo Error: Please provide at least 2 PDF files to combine.
    echo.
    pause
    exit /b 1
)

echo Combining %PDF_COUNT% PDF files...
echo.

REM Get the directory of the first PDF file
for %%A in (%1) do (
    set "OUTPUT_DIR=%%~dpA"
)

REM Generate output filename (simple, reliable method)
set "OUTPUT_FILE=combined.pdf"
set "OUTPUT_PATH=!OUTPUT_DIR!!OUTPUT_FILE!"

REM Check if file exists, add numeric suffix if needed
set "COUNTER=1"
:check_exists
if exist "!OUTPUT_PATH!" (
    set "OUTPUT_FILE=combined_!COUNTER!.pdf"
    set "OUTPUT_PATH=!OUTPUT_DIR!!OUTPUT_FILE!"
    set /A COUNTER+=1
    if !COUNTER! LSS 100 goto check_exists
)

echo Output file: !OUTPUT_FILE!
echo.

REM Run Ghostscript to combine PDFs
"!GS_PATH!" -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER -sOutputFile="!OUTPUT_PATH!" !PDF_LIST!

if errorlevel 1 (
    echo.
    echo ERROR: Failed to combine PDFs.
    echo.
    pause
    exit /b 1
)

echo.
echo Finished! Combined PDF saved to:
echo !OUTPUT_PATH!
echo.
pause
endlocal
