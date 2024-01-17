@echo off
echo.
echo ****************************************************
echo * SHUTDOWN-TIMER *
echo ****************************************************
echo.
echo Bitte geben Sie die Anzahl der Stunden bis zum Shutdown ein (z.B. 1,5).
echo Druecken Sie Enter OHNE Eingabe, um einen geplanten Shutdown abzubrechen.
echo.
set /p hours=

:: Prüfen, ob eine Eingabe erfolgt ist
if "%hours%"=="" (
    shutdown -a
    echo [INFO] Der geplante Shutdown wurde erfolgreich abgebrochen.
    pause
    exit
)

set /a seconds=%hours%*3600

:: Berechnung der Shutdown-Zeit
for /f "tokens=1-3 delims=:" %%a in ("%time%") do (
    set /a "hh=%%a"
    set /a "mm=%%b"
    set /a "ss=%%c"
)

:: Umrechnung in Sekunden und Addition
set /a "totalSecs=(hh*3600)+(mm*60)+ss+seconds"

:: Umrechnung zurück in Stunden, Minuten, Sekunden
set /a "hh=totalSecs/3600"
set /a "mm=(totalSecs%%3600)/60"
set /a "ss=totalSecs%%60"

:: Führende Nullen hinzufügen, falls nötig
if %hh% lss 10 set hh=0%hh%
if %mm% lss 10 set mm=0%mm%
if %ss% lss 10 set ss=0%ss%

shutdown -s -t %seconds%
echo [INFO] Der Computer wird in %hours% Stunden heruntergefahren.
echo [INFO] Geplante Shutdown-Zeit: %hh%:%mm%:%ss%
echo.

:: Warnung bei Eingabe von mehr als 24 Stunden
if %hours% gtr 24 (
    echo [WARNUNG] Bei einer Eingabe von mehr als 24 Stunden könnte die Zieluhrzeit ungenau sein.
)
pause
