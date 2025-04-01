import json
import csv
import argparse
import sys

def json_to_csv(json_file, csv_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as jf:
            data = json.load(jf)
    except Exception as e:
        sys.exit(f"Error reading JSON file: {e}")

    # Check if the JSON data is a list of dictionaries
    if not isinstance(data, list) or (data and not isinstance(data[0], dict)):
        sys.exit("JSON file must contain a list of dictionaries.")

    if not data:
        sys.exit("JSON file is empty.")

    # Calculate header as the union of keys from all dictionaries
    header = set()
    for row in data:
        header.update(row.keys())
    header = list(header)  # Convert to list

    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as cf:
            writer = csv.DictWriter(cf, fieldnames=header, dialect='unix')
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except Exception as e:
        sys.exit(f"Error writing CSV file: {e}")

    print(f"Successfully converted '{json_file}' to '{csv_file}'.")

def main():
    parser = argparse.ArgumentParser(
        description="Convert a JSON file to a CSV file. The JSON file must contain a list of dictionaries."
    )
    parser.add_argument("json_file", help="Path to the input JSON file")
    parser.add_argument("csv_file", help="Path to the output CSV file")
    args = parser.parse_args()

    json_to_csv(args.json_file, args.csv_file)

if __name__ == "__main__":
    main()
