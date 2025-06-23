# CopyFLP.ps1
param(
    [string]$DestinationRoot = "C:\Users\Asus\Proton Drive\hans.rudi.giger\My files\FL Studio Projects"
)

function Get-Hash {
    param([string]$Path)
    return (Get-FileHash -Algorithm SHA256 -Path $Path).Hash
}

# Sicherstellen, dass Zielroot existiert
if (-not (Test-Path $DestinationRoot)) {
    New-Item -ItemType Directory -Path $DestinationRoot -Force | Out-Null
}

$base = (Get-Location).Path.TrimEnd('\')

Get-ChildItem -Path $base -Recurse -Filter '*.flp' | ForEach-Object {
    $src = $_.FullName
    # relativer Pfad zum Basisverzeichnis
    $rel = $src.Substring($base.Length).TrimStart('\')
    $dst = Join-Path $DestinationRoot $rel
    $dstDir = Split-Path $dst -Parent

    if (-not (Test-Path $dstDir)) {
        New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
    }

    if (Test-Path $dst) {
        # Ziel existiert: Hash beider Dateien holen
        $hashSrc = Get-Hash $src
        $hashDst = Get-Hash $dst

        if ($hashSrc -eq $hashDst) {
            Write-Host "SKIP (identisch): $rel"
            return
        }

        # nicht identisch: Alter vergleichen
        $timeSrc = (Get-Item $src).LastWriteTimeUtc
        $timeDst = (Get-Item $dst).LastWriteTimeUtc

        if ($timeSrc -le $timeDst) {
            Write-Host "SKIP (Ziel neuer):  $rel"
            return
        } else {
            Write-Host "OVERWRITE (Quelle neuer): $rel"
        }
    } else {
        Write-Host "COPY:               $rel"
    }

    # Kopieren (Force überschreibt, falls vorhanden)
    Copy-Item -Path $src -Destination $dst -Force

    # Integritätsprüfung nach Kopie
    if ((Get-Hash $src) -ne (Get-Hash $dst)) {
        Write-Error "Integritätsprüfung fehlgeschlagen: $rel"
        exit 1
    }
}

Write-Host "Fertig: Alle relevanten .flp-Dateien wurden verarbeitet und verifiziert."
