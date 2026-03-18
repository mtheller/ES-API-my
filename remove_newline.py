import csv
from pathlib import Path

path_in = Path("result.csv")
path_out = Path("result_clean.csv")

with path_in.open("r", newline="", encoding="utf-8") as fin, \
     path_out.open("w", newline="", encoding="utf-8") as fout:
    reader = csv.reader(fin)
    writer = csv.writer(fout)

    for row in reader:
        cleaned = [ (value.replace("\r", " ").replace("\n", " ") if value else value)
                    for value in row ]
        writer.writerow(cleaned)
