"""
Script Name: FindAndMoveStringFromBodyToHead.py
Description: This script traverses all HTML files in the current directory and its subdirectories, searching for a specific string within the body of each document. If the string is found, it is removed from the body and added to the head of the document. This can be particularly useful for manipulating HTML files en masse, such as adding specific meta tags or scripts to the head section.

Functions:
    process_file(filepath, search_string) - Processes a single HTML file, moving the specified string from the body to the head.
    main() - Walks through the directory tree, applying process_file to each HTML file found.

Usage:
    1. Define the search_string variable with the string to move.
    2. Run the script to move the specified string from the body to the head in all HTML files in the current directory and subdirectories.
"""


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
