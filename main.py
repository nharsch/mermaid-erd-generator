#!python3
import os
import csv
import sys
import pandas
from schema import Schema, Or, Regex


CSV_DIR = "csvs"  # TODO: remove


erd_attribute = Schema((Or("str", "int", "float", "bool"),  # Supports the SQLITE minimum set + bool
                        Regex("^\S*$")))                    # Non empty strings for names

def clean_field(field):
    return field.strip()\
                .replace(" ", "-")  # slugify spaces

def abstract_type_from_dtype(dtype):
    dstr = str(dtype)
    if dstr == "object":
        return "str"
    if dstr == "int64":
        return "int"
    if dstr == "float64":
        return "float"
    if dstry == "boolean":
        return "bool"
    return dstr

class ERDBlock(object):
    def __init__(self, entity_name: str, attributes: erd_attribute):
        self.entity_name = entity_name
        for attribute in attributes:
            erd_attribute.validate(attribute)
        self.attributes = attributes

    def __repr__(self):
        return self.erd_string

    @classmethod
    def from_csv(cls, path):
        """
        entity_name: name of entity
        csv_string: csv string where first row contains headers
        """
        with open(path) as csv_file:
            entity_name = clean_field(os.path.basename(path).replace(".csv", ""))
            dataframe = pandas.read_csv(csv_file)
            dataframe.columns = [clean_field(col) for col in dataframe.columns]
            attributes = [(abstract_type_from_dtype(dataframe[col].dtype), col)\
                          for col in dataframe.columns]
            return cls(entity_name, attributes)

    @classmethod
    def from_SQL(cls):
        # TODO
        pass

    @property
    def erd_string(self):
        # TODO: how to fix whitespacing
        erd_str = "{entity_name} {{ {attributes} }}".format(entity_name="TABLE__{}".format(self.entity_name.upper()),
                                                            attributes=" ".join(("{} {}".format(c[0], c[1]) for c in self.attributes)))
        return erd_str


class ERDDiagram(object):

    def __init__(self, blocks):
        self.blocks = blocks

    def __repr__(self):
        return self.erd_string

    @classmethod
    def from_csv_dir(cls, csv_dir):
        blocks = []
        for filename in os.listdir(csv_dir):
            path = os.path.join(CSV_DIR, filename)
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
