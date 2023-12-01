import imageio
import os


def bilder_zu_video(output_name="output.mp4", fps=15):
    # Liste alle Dateien im aktuellen Verzeichnis auf
    dateien = [f for f in os.listdir() if os.path.isfile(f)]

    # Filtere nur Bilddateien heraus
    bilddateien = [
        f
        for f in dateien
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"))
    ]

    # Sortiere Bilddateien (optional, falls Sie eine bestimmte Reihenfolge möchten)
    bilddateien.sort()

    # Lade alle Bilder
    bilder = [imageio.imread(bild) for bild in bilddateien]

    # Schreibe die Bilder in ein MP4-Video
    imageio.mimsave(output_name, bilder, fps=fps)

    print(f"Video wurde als {output_name} gespeichert.")


if __name__ == "__main__":
    bilder_zu_video()
