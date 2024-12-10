import csv
import json
import requests

URL = 'https://opendata.stadt-muenster.de/sites/default/files/M%C3%BCnster-BabyVornamenHitliste_2023.csv'
YEARS = 7
TOP_N_COUNT = 15

# Datei herunterladen
response = requests.get(URL)
response.raise_for_status()  # Überprüfen, ob der Download erfolgreich war

# Inhalt der CSV-Datei auslesen
csv_content = response.text

# CSV-Daten mit DictReader parsen
fieldnames = ("year","rank","sex","name","count")
csv_reader = csv.DictReader(csv_content.splitlines(), fieldnames, delimiter=";", restkey="crap")

# Iterieren durch die Zeilen der CSV-Datei
list_jungen = []
list_maedchen = []
rownr = 0
for row in csv_reader:
    rownr = rownr + 1
    if rownr == 1:
        continue
    if int(row['rank']) > TOP_N_COUNT:
        continue
    if int(row['year']) < (2024-YEARS):
        continue

    row.pop('crap', None)
    if row['sex'] == "Junge":
        list_jungen.append(row)
    else:
        list_maedchen.append(row)

print(json.dumps({
    'womens': list_maedchen,
    'mens': list_jungen,
    'MONTHS_OF_DATA': YEARS,
    'TOP_N_COUNT': TOP_N_COUNT
}))
