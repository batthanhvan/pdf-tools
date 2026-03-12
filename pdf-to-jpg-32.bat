@echo off
setlocal enabledelayedexpansion
set bat_file=%~dp0%pdf-to-jpg.bat
call "%bat_file%" "bin\gswin32c.exe" %*