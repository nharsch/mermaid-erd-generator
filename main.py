#!python3
import os
import csv
import sys
from schema import Schema, Or


CSV_DIR = "csvs"

# print("erDiagram")
# for filename in os.listdir(CSV_DIR):
#     path = os.path.join(CSV_DIR, filename)
#     with open(path) as file:
#         reader = csv.reader(file)
#         table_name = filename.replace(".csv", "")
#         headers = next(reader)
#         erd_str = "{table_name} {{ {columns} }}".format(table_name=table_name.upper(),
#                                                         columns="\n".join("string {}".format(c) for c in headers))

#         print(erd_str)

# Supports the SQLITE minimum set + bool
erd_attribute = Schema((str, Or(str, int, float, bool, None)))



class ERDBlock(object):
    def __init__(self, entity_name: str, attributes: erd_attribute):
        self.entity_name = entity_name
        self.attributes = attributes

    @classmethod
    def from_csv(cls, path):
        """
        entity_name: name of entity
        csv_string: csv string where first row contains headers
        """
        with open(path) as csv_file:
            reader = csv.reader(csv_file)
            entity_name = os.path.basename(path).replace(".csv", "")
            headers = next(reader)
            # TODO: try to guess data type given values
            attributes = [('string', h) for h in headers]
            return cls(entity_name, attributes)

    @classmethod
    def from_SQL(cls):
        # TODO
        pass

    @property
    def erd_string(self):
        # TODO: how to fix whitespacing
        erd_str = "{entity_name} {{ {attributes} }}".format(entity_name=self.entity_name.upper(),
                                                            attributes="\n".join(("{} {}".format(c[0], c[1]) for c in self.attributes)))
        return erd_str


class ERDDiagram(object):

    def __init__(self, blocks):
        self.blocks = blocks

    @classmethod
    def from_csv_dir(cls, csv_dir):
        blocks = []
        for filename in os.listdir(csv_dir):
            path = os.path.join(CSV_DIR, filename)
            table_name = filename.replace(".csv", "")
            erd_block = ERDBlock.from_csv(path)
            blocks.append(erd_block)
        return cls(blocks)

    @classmethod
    def from_sql(cls, sql_str):
        # TODO
        pass

    @property
    def erd_string(self):
        return "erDiagram\n{}".format("\n".join(b.erd_string for b in self.blocks))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        CSV_DIR = sys.argv[1]
    diagram = ERDDiagram.from_csv_dir(CSV_DIR)
    print(diagram.erd_string)
