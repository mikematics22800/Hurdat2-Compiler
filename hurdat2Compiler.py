import csv
import json
import os

# Open the HURDAT2 data file and read all lines
with open("hurdat2.txt", "r") as file:
    lines = file.readlines()

# Initialize metadata list
metadata = []

# Process each line in the HURDAT2 data file
for line in lines:
    values = line.split(",")
    values = [value.strip() for value in values]
    # Check if the line contains storm metadata (3 values)
    if len(values) == 4:        
        # Update the year and create storm ID and CSV path 
        year = int(values[0][-4:])
        name = values[1].capitalize()
        id = f"{values[0]}_{name}"
        # Append metadata to list for later use
        metadata.append([year, name, id])
        csv_path = f"./hurdat2_csv/{year}/{id}.csv"
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        # Create directories and write the CSV header if the file does not exist
        with open(csv_path, "w", newline="") as csv_file:
            if year < 2004:
                csv_file.write("date,time_utc,record,status,lat,lng,max_wind_kt,min_pressure_mb\n")
            else:
                csv_file.write("date,time_utc,record,status,lat,lng,max_wind_kt,min_pressure_mb,34kt_wind_nm,50kt_wind_nm,64kt_wind_nm\n")
    else:
        # Append the line to the existing CSV file
        with open(csv_path, "a", newline="") as csv_file:
            if year < 2004:
                csv_file.write(",".join(values[:8]) + "\n")
            else:
                wind_nm = values[8:]
                _34kt_wind_nm = "/".join(wind_nm[:4])
                _50kt_wind_nm = "/".join(wind_nm[4:8])
                _64kt_wind_nm = "/".join(wind_nm[8:12])
                csv_file.write(",".join(values[:8]) + f",{_34kt_wind_nm},{_50kt_wind_nm},{_64kt_wind_nm}\n")

# Initialize season list and reset year
season = []
year = 1851

# Process each value in the metadata list
for values in metadata:
    json_path = f"./hurdat2_json/{year}.json" 
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    if year != int(values[0]):
        with open(json_path, "w") as json_file:
            json.dump(season, json_file, indent=2)
        season = []
    year = values[0]
    name = values[1]
    id = values[2]
    csv_path = f"./hurdat2_csv/{year}/{id}.csv"
    data = []
    with open(csv_path, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            for key, value in row.items():
                # Convert latitude and longitude to float
                if key == 'lat' or key == 'lng':
                    if key == 'lat':
                        row[key] = float(value[:-1])
                    else:
                        row[key] = -float(value[:-1])
                else:
                    if key != "date" and key != "time_utc":
                        if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                            row[key] = int(value)
                        else: 
                            row[key] = value
                    else:
                        row[key] = value
                if "nm" in key:
                    radii = [int(x) for x in value.split('/')]
                    row[key] = dict(zip(["ne", "se", "sw", "nw"], radii))
            data.append(row)
        
        # Create a storm dictionary and append it to the season list
        storm = {
            "id": id,
            "image": "",
            "fatalities": 0,
            "cost_usd": 0,
            "retired": "false",
            "data": data
        }
        season.append(storm)

# Write the JSON file for the last year
json_path = f"./hurdat2_json/{year}.json"
with open(json_path, "w") as json_file:
    json.dump(season, json_file, indent=2)