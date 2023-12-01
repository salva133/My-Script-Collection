import os
from bs4 import BeautifulSoup


def process_file(filepath, search_string):
    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    body = soup.body
    head = soup.head

    if body and head and search_string in body.get_text():
        # Fügen Sie hier den Code ein, um den String zu verschieben, z.B.:
        body.string.replace_with(body.string.replace(search_string, ""))
        head.string.replace_with(search_string + head.string)

        # Speichern Sie die Änderungen
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(str(soup))


def main():
    search_string = (
        "IHR_STRING"  # Ersetzen Sie "IHR_STRING" durch den gewünschten String
    )

    for dirpath, dirnames, filenames in os.walk("."):
        for filename in filenames:
            if filename.endswith(".html"):
                process_file(os.path.join(dirpath, filename), search_string)


if __name__ == "__main__":
    main()
