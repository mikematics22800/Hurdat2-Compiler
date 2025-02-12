import csv
import json
import os

with open("atl.txt", "r") as file:
    atl = file.readlines()

with open("pac.txt", "r") as file:
    pac = file.readlines()

def export_hurdat(lines, startYear, basin):
    metadata = []
    for line in lines:
        values = line.split(",")
        values = [value.strip() for value in values]
        if len(values) == 4:        
            year = int(values[0][-4:])
            name = values[1].capitalize()
            id = f"{values[0]}_{name}"
            metadata.append([year, name, id])
            csv_path = f"./{basin}/csv/{year}/{id}.csv"
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            
            with open(csv_path, "w", newline="") as csv_file:
                if year < 2004:
                    csv_file.write("date,time_utc,record,status,lat,lng,max_wind_kt,min_pressure_mb\n")
                else:
                    csv_file.write("date,time_utc,record,status,lat,lng,max_wind_kt,min_pressure_mb,34kt_wind_nm,50kt_wind_nm,64kt_wind_nm\n")
        else:
            with open(csv_path, "a", newline="") as csv_file:
                if year < 2004:
                    csv_file.write(",".join(values[:8]) + "\n")
                else:
                    wind_nm = values[8:]
                    _34kt_wind_nm = "/".join(wind_nm[:4])
                    _50kt_wind_nm = "/".join(wind_nm[4:8])
                    _64kt_wind_nm = "/".join(wind_nm[8:12])
                    csv_file.write(",".join(values[:8]) + f",{_34kt_wind_nm},{_50kt_wind_nm},{_64kt_wind_nm}\n")

    season = []
    year = startYear

    for values in metadata:
        json_path = f"./{basin}/json/{year}.json" 
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        if year != int(values[0]):
            with open(json_path, "w") as json_file:
                json.dump(season, json_file, indent=2)
            season = []
        year = values[0]
        name = values[1]
        id = values[2]
        csv_path = f"./{basin}/csv/{year}/{id}.csv"
        data = []
        with open(csv_path, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                for key, value in row.items():
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
            
            storm = {
                "id": id,
                "data": data
            }
            season.append(storm)

    json_path = f"./{basin}/json/{year}.json"
    with open(json_path, "w") as json_file:
        json.dump(season, json_file, indent=2)

export_hurdat(atl, 1851, 'atl')
export_hurdat(pac, 1949, 'pac')