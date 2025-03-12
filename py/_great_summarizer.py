import os

abs_path = r"C:\Users\Tony\Desktop"
output_file = os.path.join(abs_path, "Script_Collection.txt")

def main():
    # Alle .py-Dateien im aktuellen Verzeichnis sammeln
    py_files = [f for f in os.listdir() if f.endswith(".py") and f != __file__]

    # Inhalte der .py-Dateien sammeln und in summary.txt speichern
    with open(output_file, "w", encoding="utf-8") as summary:
        for py_file in py_files:
            summary.write(f"# Inhalt von {py_file}\n\n")
            with open(py_file, "r", encoding="utf-8") as file:
                summary.write(file.read())
                summary.write("\n\n" + "=" * 40 + "\n\n")

    print(f"Zusammenfassung abgeschlossen. Siehe {output_file}")

if __name__ == "__main__":
    main()
