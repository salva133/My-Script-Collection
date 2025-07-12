import os
import pytest

from transfer_audio_to_cloud import (
    erstelle_verzeichnis,
    kopiere_audiodateien,
    erstelle_backup,
    stelle_backup_wieder_her_fuer_ziel
)

@pytest.fixture
def testdirs(tmp_path):
    # Lege temporäre Quell- und Zielverzeichnisse an
    source = tmp_path / "quelle"
    target = tmp_path / "ziel"
    backup_dir = tmp_path / "backup"
    source.mkdir()
    target.mkdir()
    backup_dir.mkdir()
    # Dummy-Audiodatei erzeugen
    dummy_file = source / "track1.mp3"
    dummy_file.write_text("audio-daten")
    yield {
        "source": str(source),
        "target": str(target),
        "backup_dir": str(backup_dir),
        "dummy_file": str(dummy_file),
    }
    # Aufräumen macht pytest/Fixture automatisch

def test_erstelle_verzeichnis_loescht_inhalt(testdirs, monkeypatch):
    # Zielverzeichnis mit Datei befüllen
    test_file = os.path.join(testdirs["target"], "abc.mp3")
    with open(test_file, "w") as f:
        f.write("daten")
    # Patch das Backup-Verzeichnis auf das Testverzeichnis
    monkeypatch.setattr("transfer_audio_to_cloud.backup_verzeichnis", testdirs["backup_dir"])
    erstelle_verzeichnis(testdirs["target"])
    assert not os.listdir(testdirs["target"])

def test_kopiere_audiodateien(testdirs):
    kopiere_audiodateien(testdirs["source"], testdirs["target"])
    files = os.listdir(testdirs["target"])
    assert "track1.mp3" in files

def test_erstelle_backup_und_restore(testdirs, monkeypatch):
    # Datei ins Ziel kopieren
    kopiere_audiodateien(testdirs["source"], testdirs["target"])
    # Patch das Backup-Verzeichnis auf das Testverzeichnis
    monkeypatch.setattr("transfer_audio_to_cloud.backup_verzeichnis", testdirs["backup_dir"])
    # Backup erstellen
    erstelle_backup(testdirs["target"])
    # Datei im Ziel löschen, um Restore zu testen
    for f in os.listdir(testdirs["target"]):
        os.remove(os.path.join(testdirs["target"], f))
    assert not os.listdir(testdirs["target"])
    # Restore durchführen
    stelle_backup_wieder_her_fuer_ziel(testdirs["target"])
    files = os.listdir(testdirs["target"])
    assert "track1.mp3" in files
