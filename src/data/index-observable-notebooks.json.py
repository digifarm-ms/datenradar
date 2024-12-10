import os
import logging
import json
from datetime import datetime

# Basic logger configuration
logging.basicConfig(level=logging.DEBUG, format='<%(asctime)s %(levelname)s> %(message)s')

LOGGER = logging.getLogger(__name__)
TODAY = datetime.now()

# LOGGER.info("=====> CHECK START %s <=====", TODAY)


# Funktion, um den Titel aus einer Markdown-Datei zu extrahieren
def extract_title_from_markdown(filepath):
    title = ""
    desc = ""

    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            # Prüfen, ob die Zeile mit '#' beginnt (Markdown-Titel)
            if line.startswith("# "):
                desc = line[1:].strip()
            if line.startswith("title: "):
                title = line[6:].strip()

    return title, desc

# Pfad zum Verzeichnis mit den Markdown Dateien erzeugen
parent_dir = os.path.abspath(os.path.join(os.getcwd(), "src"))
if os.getcwd().endswith("data"):
    # Wenn man's manuell im data verzeichnis aufruf, dann soll's auch gehen
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Liste aller Markdown-Dateien erzeugen
markdown_files = [
    os.path.join(parent_dir, f) for f in os.listdir(parent_dir) if f.endswith('.md')
]


# Markdown-Dateien einlesen und Infos extrahieren
titles = []
for md_file in markdown_files:
    title, desc = extract_title_from_markdown(md_file)
    if title:
        titles.append({"file": os.path.basename(md_file).replace(".md", ".html"), "title": title, "desc": desc})


print(json.dumps(titles))
