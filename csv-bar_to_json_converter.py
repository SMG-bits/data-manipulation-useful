import csv
import json
import tkinter as tk
from tkinter import filedialog
import os

def clean_value(value):
    if isinstance(value, str):
        return value.strip()
    elif isinstance(value, list):
        return [clean_value(v) for v in value if v]
    return value

def csv_to_json(csv_file_path, json_file_path):
    data = []
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            # Read a sample to check for header
            sample = csvfile.read(1024)
            csvfile.seek(0)
            
            if not sample:
                print("The CSV file is empty.")
                return

            # Use '|' as the delimiter
            has_header = csv.Sniffer().has_header(sample)
            
            csvreader = csv.DictReader(csvfile, delimiter='|', fieldnames=None if has_header else [f"column_{i}" for i in range(len(sample.split('|')))])
            
            for row in csvreader:
                cleaned_row = {k: clean_value(v) for k, v in row.items() if v}
                if cleaned_row:  # Only append non-empty rows
                    data.append(cleaned_row)
            
        if not data:
            print("No data found in the CSV file.")
            return

    except csv.Error as e:
        print(f"CSV Error: {e}")
        return
    except IOError as e:
        print(f"I/O Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error while reading CSV: {e}")
        return

    try:
        with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        print(f"Conversion complete. JSON file saved as {json_file_path}")
    except IOError as e:
        print(f"I/O Error while writing JSON: {e}")
    except Exception as e:
        print(f"Unexpected error while writing JSON: {e}")

# Create a root window and hide it 
root = tk.Tk()
root.withdraw()

# Open file dialog to select CSV file
csv_file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
if not csv_file_path:
    print("No file selected. Exiting.")
    exit()

# Get the directory of the selected CSV file
json_file_path = os.path.splitext(csv_file_path)[0] + '.json'

csv_to_json(csv_file_path, json_file_path)