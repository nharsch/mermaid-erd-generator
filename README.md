# Mermaid ERD Generator

General Purpose Tool for generating [Mermaid.js ERD Diagrams](https://mermaid-js.github.io/mermaid/#/./entityRelationshipDiagram)

## Importing From CSVs

Given a `csv_directory` of csv files representing entities (IE: each file is a SQL dumps of a table), run `./main.py csv_directory`.

-- or --

Add CSV files to `csvs` directory and uun `./main.py`

This will print a Mermaid ERD Diagram with Entities for each CSV file. CSV Header rows will be used to generate entitiy attributes. By default, all entity attributes will be `string` data types.

This printed diagram string can be previewed using a Mermaid preview tool like [Mermaid Live](https://mermaid.live/edit#pako:eNpFj8EKwjAMhl-l5Lwn6E3QnQTBeSxIXLNZaNORpQcZe3crDHv7Avn-5N9gzJ7AAsk54CyYHA-PU9-bzawqgWfDmMjxMeDc2OfXnyVHMrvj--16GZqrQWMTwvpMyDVCWgYtKJqI9WdDB4kkYfD1o82xMQ70TfU-2IqeJixRHTje6yoWzcOHR7AqhTooi0elowbYCeNK-xdDclGN)

![Test Diagram](./test-diagram.png)
