@echo off
set /p hours="Geben Sie die Anzahl der Stunden bis zum Shutdown ein (z.B. 1,5): "
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
echo Computer wird in %hours% Stunden heruntergefahren.
echo Geplante Shutdown-Zeit: %hh%:%mm%:%ss%

:: Warnung bei Eingabe von mehr als 24 Stunden
if %hours% gtr 24 (
    echo Warnung: Bei einer Eingabe von mehr als 24 Stunden wird die Zieluhrzeit möglicherweise nicht korrekt angegeben, weil dieses Skript einfach grenzdebil und schnell-schnell zusammengezimmert wurde.
)
pause
