import csv
import json
import tkinter as tk
from tkinter import filedialog

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

            # Try to detect the delimiter // Inițiază dedectarea delimitatorului // works with , and ; // On MacOS errors with | // use alternative csv-bar_to_json_converter.py
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            csvreader = csv.DictReader(csvfile, dialect=dialect)
            
            for row in csvreader:
                cleaned_row = {k: clean_value(v) for k, v in row.items() if v}
                data.append(cleaned_row)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    try:
        with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        print(f"Conversion complete. JSON file saved as {json_file_path}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

# Create a root window and hide it 
root = tk.Tk()
root.withdraw()

# Open file dialog to select CSV file // Deschide fereastra pentru căutarea fișierului CSV
csv_file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])

if not csv_file_path:
    print("No file selected. Exiting.")
    exit()

# Get the directory of the selected CSV file // Accesează directorul sursă în care plasează JSON-ul rezultat
json_file_path = csv_file_path.rsplit('.', 1)[0] + '.json'

csv_to_json(csv_file_path, json_file_path)
