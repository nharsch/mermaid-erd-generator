#!python3
import csv
import os
import re
import sys
import pandas
from fuzzywuzzy import fuzz
from schema import Schema, Or, Regex


CSV_DIR = "csvs"  # TODO: remove

rel_type = Or("one-to-one", "one-to-many", "many-to-many")
erd_attribute = Schema((Or("str", "int", "float", "bool"),  # Supports the SQLITE minimum set + bool
                        Regex("^\S*$")))                    # Non empty strings for names


def clean_field(field):
    field = field.strip().replace(" ", "-").replace(".", "")
    if re.match("^[^a-zA-Z].*", field):
        # TODO: is there a better way?
        field = f"SAFE__{field}"
    if not field:
        return "blank"
    return field

def clean_entity_name(entity_name):
    if re.match("^[^a-zA-Z].*", entity_name):
        # TODO: is there a better way?
        entity_name = f"SAFE__{entity_name}"
    return entity_name.upper()

def abstract_type_from_dtype(dtype):
    """attempt to get data datatype of column"""
    dstr = str(dtype)
    if dstr == "int64":
        return "int"
    if dstr == "float64":
        return "float"
    if dstr == "boolean":
        return "bool"
    return "str"

def sql_type_from_abstract_type(atype):
    if atype == "int":
        return "INTEGER"
    if atype == "float64":
        return "REAL"
    if atype == "boolean":
        return "INTEGER"
    return "TEXT"



def attribute_to_sql_column_string(attribute: erd_attribute):
    sql_type = sql_type_from_abstract_type(attribute[0])
    attr_name = clean_field(attribute[1])
    return f"{attr_name} {sql_type}"
    pass


class ERDBlock(object):
    def __init__(self, entity_name: str, attributes: list[erd_attribute]):
        self.entity_name = clean_entity_name(entity_name)
        self.attributes = attributes

    def __repr__(self):
        return self.erd_string

    @classmethod
    def from_csv(cls, path):
        """
        entity_name: name of entity
        csv_string: csv string where first row contains headers
        """
        entity_name = clean_field(os.path.basename(path).replace(".csv", ""))
        dataframe = pandas.read_csv(path, encoding_errors="ignore", low_memory=False, on_bad_lines="skip")
        # clean up columnd names
        dataframe.columns = [clean_field(col) for col in dataframe.columns]
        dataframe = dataframe.loc[:, ~dataframe.columns.str.contains('^Unnamed')]
        # find types
        table_attributes = []
        for col in dataframe.columns:
            if col:
                try:
                    dstring = abstract_type_from_dtype(dataframe[col].dtype)
                except AttributeError:
                    dstring = "str"
            table_attributes.append((dstring, col))
        return cls(entity_name, table_attributes)

    @classmethod
    def from_SQL(cls):
        # TODO
        pass

    @property
    def sql_string(self):
        # TODO
        column_statements = ",\n".join(attribute_to_sql_column_string(attr) for attr in self.attributes)
        return """
        CREATE TABLE IF NOT EXISTS {table_name} (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        {columns}
        )
        """.format(table_name=self.entity_name, columns=column_statements)


    @property
    def erd_string(self):
        attributes=" ".join(("{} {}".format(c[0], c[1]) for c in self.attributes))
        return f"{self.entity_name} {{ {attributes} }}"


class ERDRelation(object):
    def __init__(self, from_name: str, to_name: str, rel_type: rel_type, label: str = None):
        self.from_name = from_name
        self.to_name = to_name
        self.rel_type = rel_type
        self.label = label

    def __repr__(self):
        return self.erd_string

    @property
    def rel_str(self):
        if self.rel_type == "one-to-one":
            return "||--||"
        if self.rel_type == "one-to-many":
            return "||--o{"
        if self.rel_type == "many-to-many":
            return "}o--o{"

    @property
    def erd_string(self):
        return f"{self.from_name} {self.rel_str} {self.to_name} : {self.label}"

    @property
    def sql_str(self):
        pass


def find_relations(blocks: list[ERDBlock]):
    relations = []
    for current_block in blocks:
        for typ, attr in current_block.attributes:
            ranks = [(block.entity_name, fuzz.token_sort_ratio(attr, block.entity_name))
                     for block in blocks
                     if fuzz.token_sort_ratio(attr, block.entity_name) > 75
                     and block != current_block]
            if len(ranks):
                entity_name, confidence_level = max(ranks, key=lambda x: x[1])
                rel = ERDRelation(entity_name,
                                current_block.entity_name,
                                rel_type="one-to-many",
                                label=f'"{confidence_level}% confidence match on {current_block.entity_name}.{attr}"')
                relations.append(rel)
    return relations


class ERDDiagram(object):

    def __init__(self, blocks: list[ERDBlock], relations: list[ERDRelation]):
        self.blocks = blocks
        self.relations = relations

    def __repr__(self):
        return self.erd_string

    @classmethod
    def from_csv_dir(cls, csv_dir):
        blocks = []
        for filename in os.listdir(csv_dir):
            path = os.path.join(CSV_DIR, filename)
            erd_block = ERDBlock.from_csv(path)
            blocks.append(erd_block)
            relations = find_relations(blocks)
        return cls(blocks, relations)

    @classmethod
    def from_sql(cls, sql_str):
        pass

    @property
    def sql_string(self):
        # TODO render create statements for relationships
        return "\n\n".join(block.sql_string for block in self.blocks)



    @property
    def erd_string(self):
        return "erDiagram\n{}\n{}".format("\n".join(b.erd_string for b in self.blocks),
                                          "\n".join(rel.erd_string for rel in self.relations))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        CSV_DIR = sys.argv[1]
    diagram = ERDDiagram.from_csv_dir(CSV_DIR)
    print(diagram.erd_string)
