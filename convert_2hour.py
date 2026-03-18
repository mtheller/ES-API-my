import csv

def duration_to_hours(duration: str) -> float:
    """
    Erwartet Format: HH:MM:SS:MS (Millisekunden)
    Gibt Dauer in Stunden zurück.
    """
    if not duration:
        return 0.0

    parts = duration.split(":")
    if len(parts) != 4:
        return 0.0

    hh = int(parts[0])
    mm = int(parts[1])
    ss = int(parts[2])
    ms = int(parts[3])  # Millisekunden

    seconds = hh * 3600 + mm * 60 + ss + ms / 1000.0
    hours = seconds / 3600.0
    return hours

input_file = "result_clean.csv"
output_file = "result_clean_h.csv"

with open(input_file, newline="", encoding="utf-8") as f_in, \
     open(output_file, "w", newline="", encoding="utf-8") as f_out:

    reader = csv.DictReader(f_in)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        try:
            dur = row.get("Duration", "")
            hours = duration_to_hours(dur)
            row["Duration"] = f"{hours:.4f}"  # z.B. 0.0006 h
        except Exception:
            # Bei Fehler Zeile unverändert schreiben
            pass

        writer.writerow(row)
