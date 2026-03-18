# get_metadata_allClips.py

## Übersicht

Dieses Skript extrahiert Metadaten aller Clips aus einer FlowAPI-Instanz und speichert sie in einer CSV-Datei (`result.csv`). Es werden zahlreiche Metadatenfelder sowie benutzerdefinierte Felder ausgelesen und übersichtlich exportiert.

## Voraussetzungen

- Python 3.x
- Die Python-Pakete:
  - `FlowAPI`
  - `python-dotenv`
- Eine gültige `cred.env`-Datei im gleichen Verzeichnis mit den Zugangsdaten:
  ```
  FLOW_USER=dein_benutzername
  FLOW_PASSWORD=dein_passwort
  FLOW_HOST=dein_host
  ```

## Funktionsweise

1. Das Skript lädt die Zugangsdaten aus der `cred.env`.
2. Es verbindet sich mit der FlowAPI und liest alle verfügbaren Clips aus.
3. Für jeden Clip werden relevante Metadaten und benutzerdefinierte Felder extrahiert.
4. Die Daten werden zeilenweise in die Datei `result.csv` geschrieben.
5. Bereits vorhandene Zeilen werden nicht überschrieben, sondern neue Clips werden angehängt.

## Wichtige Felder im Export

- Clipname, Project, Captured, Modified, Media Space, Status, File Type, Video Codec, Width, Height, Frame Rate, Audio File Type, Audio Bit Depth, Audio Sample Rate, Start, End, Duration, Comment
- Diverse benutzerdefinierte Felder wie Mapping Identifier, Rights Owner, Production Year, Genre, Accounting ID, usw.

## Hinweise

- Das Skript kann bei sehr großen Datenmengen längere Zeit laufen.
- Die Funktion `duration_tc_ms` berechnet die Dauer eines Clips anhand der Timecodes.
- Die CSV-Datei wird im UTF-8-Format geschrieben.

## Ausführung

```bash
python get_metadata_allClips.py
```
