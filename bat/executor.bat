@echo off
setlocal enabledelayedexpansion

:: Zählt die Anzahl der Python-Dateien im aktuellen Verzeichnis
set /a count=0
for %%x in (*.py) do (
    set /a count+=1
    set "file!count!=%%x"
)

:: Prüft, ob nur eine Python-Datei vorhanden ist und führt diese direkt aus
if %count%==1 (
    python "!file1!"
    goto end
)

:: Bietet eine Auswahl, wenn mehrere Python-Dateien vorhanden sind
echo Gefundene Python-Dateien:
for /l %%i in (1,1,%count%) do (
    echo %%i. !file%%i!
)

:choose
echo Wählen Sie eine Datei durch Eingabe der entsprechenden Nummer (1-%count%):
set /p choice="Auswahl: "
if !choice! lss 1 or !choice! gtr %count% (
    echo Ungültige Auswahl. Bitte versuchen Sie es erneut.
    goto choose
)

:: Führt die gewählte Python-Datei aus
python "!file%choice%!"
pause

:end
endlocal
