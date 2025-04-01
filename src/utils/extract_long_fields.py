# extract prose fields from records.

import json
import csv
import argparse
import sys

PROSE_FIELDS= ['decoration_description', 'sources_used', 'primary_citation', 'other_bibliography', 'essay_number', 'essay_text']
REDUCED_FIELDS = ['id'] + PROSE_FIELDS

def excised_record(record):
    return {k: v for k,v in record.items() if k in REDUCED_FIELDS}
    

def reduced_record(record):
    return {k: v for k,v in record.items() if k not in PROSE_FIELDS}


def reduced_records(records):
    return [reduced_record(record) for record in records]


def excised_records(records):
    return [excised_record(record) for record in records]


def save_data(data, fname):
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



def main():
    parser = argparse.ArgumentParser(
        description="Convert a JSON file to a CSV file, exporting only the id and description fields."
    )
    parser.add_argument("json_file", help="Path to the input JSON file")
    parser.add_argument("out_excised_file", help="Path to the file of excised fields")
    parser.add_argument("out_reduced_file", help="Path to the file of reduced records")
    args = parser.parse_args()

    with open(args.json_file, 'r', encoding='utf-8') as f:
        records = json.load(f)

    reduced_data = reduced_records(records)
    excised_data = excised_records(records)
    save_data(reduced_data, args.out_reduced_file)
    save_data(excised_data, args.out_excised_file)



if __name__ == "__main__":
    main()
