# CopyFLP.ps1
param(
    # Statisches Quellverzeichnis
    [string]$SourceRoot      = "C:\Users\Asus\Documents\Image-Line\FL Studio\Projects",
    # Statisches Zielverzeichnis
    [string]$DestinationRoot = "C:\Users\Asus\Proton Drive\hans.rudi.giger\My files\FL Studio Projects"
)

function Get-Hash {
    param([string]$Path)
    return (Get-FileHash -Algorithm SHA256 -Path $Path).Hash
}

# Stelle sicher, dass Quell- und Zielordner existieren
if (-not (Test-Path $SourceRoot)) {
    Write-Error "Quellverzeichnis existiert nicht: $SourceRoot"
    exit 1
}
if (-not (Test-Path $DestinationRoot)) {
    New-Item -ItemType Directory -Path $DestinationRoot -Force | Out-Null
}

# Alle .flp-Dateien im Quellverzeichnis finden, Backup-Ordner ignorieren
Get-ChildItem -Path $SourceRoot -Recurse -Filter '*.flp' |
    Where-Object { $_.FullName -notmatch '\\Backup\\' } |
    ForEach-Object {
        $src     = $_.FullName
        # relativer Pfad zum Quellverzeichnis
        $rel     = $src.Substring($SourceRoot.Length).TrimStart('\')
        $dst     = Join-Path $DestinationRoot $rel
        $dstDir  = Split-Path $dst -Parent

        if (-not (Test-Path $dstDir)) {
            New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
        }

        if (Test-Path $dst) {
            $hashSrc = Get-Hash $src
            $hashDst = Get-Hash $dst

            if ($hashSrc -eq $hashDst) {
                Write-Host "SKIP (identisch): $rel"
                return
            }

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

        Copy-Item -Path $src -Destination $dst -Force

        if ((Get-Hash $src) -ne (Get-Hash $dst)) {
            Write-Error "Integritätsprüfung fehlgeschlagen: $rel"
            exit 1
        }
    }

Write-Host "Fertig: Alle relevanten .flp-Dateien wurden verarbeitet und verifiziert."
