@echo off
setlocal

:: Überprüfen, ob Quell- und Zielverzeichnis als Parameter übergeben wurden
if "%~1"=="" (
  echo Fehler: Kein Quellverzeichnis angegeben.
  echo Nutzung: syncer_wrapper.bat "Quellverzeichnis" "Zielverzeichnis"
  pause
  exit /b 1
)
if "%~2"=="" (
  echo Fehler: Kein Zielverzeichnis angegeben.
  echo Nutzung: syncer_wrapper.bat "Quellverzeichnis" "Zielverzeichnis"
  pause
  exit /b 1
)

:: Aufruf des Hauptskripts mit den übergebenen Parametern
call sync.bat "%~1" "%~2"

endlocal
