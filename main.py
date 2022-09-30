#!python3
import os
import csv

CSV_DIR = "csvs"

print("erDiagram")
for filename in os.listdir(CSV_DIR):
    path = os.path.join(CSV_DIR, filename)
    with open(path) as file:
        reader = csv.reader(file)
        table_name = filename.replace(".csv", "")
        headers = next(reader)
        erd_str = "{table_name} {{ {columns} }}".format(table_name=table_name.upper(),
                                                        columns="\n".join("string {}".format(c) for c in headers))

        print(erd_str)


