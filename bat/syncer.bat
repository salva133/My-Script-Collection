@echo off
setlocal

:: Prüfe, ob beide Parameter übergeben wurden
if "%~1"=="" (
  echo Fehler: Kein Quellverzeichnis angegeben.
  echo Nutzung: syncer.bat "Quellverzeichnis" "Zielverzeichnis"
  pause
  exit /b 1
)
if "%~2"=="" (
  echo Fehler: Kein Zielverzeichnis angegeben.
  echo Nutzung: syncer.bat "Quellverzeichnis" "Zielverzeichnis"
  pause
  exit /b 1
)

:: Parameter übernehmen
set "SOURCE=%~1"
set "TARGET=%~2"

:: Mit /MIR wird das Ziel exakt zum Spiegel des Quellverzeichnisses – auch überzählige Dateien werden gelöscht.
robocopy "%SOURCE%" "%TARGET%" /MIR

echo Synchronisation abgeschlossen.
pause
endlocal
