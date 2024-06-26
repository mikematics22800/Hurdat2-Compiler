import csv
import json
import os

with open("hurdat2.txt", "r") as file:
    lines = file.readlines()

year = "1851"
season = []

for line in lines:
    values = line.split(",")
    values = [value.strip() for value in values]
    if len(values) == 4:
        if year != values[0][-4:]:
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, "w") as file:
                json.dump(season, file, indent=2)
            season = []
        year = values[0][-4:]
        name = values[1]
        id = f"{values[0]}_{name}"
        csv_path = f"./hurdat2_csv/{year}/{id}.csv"
        json_path = f"./hurdat2_json/{year}.json" 
        if os.path.exists(csv_path):
            data=[]
            with open(csv_path, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    for key, value in row.items():
                        value = value.replace(" ", "")
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
                    data.append(row)
            storm = {
                "id": id,
                "image": "",
                "fatalaties": 0,
                "cost_usd": 0,
                "retired": "false",
                "data": data
            }
            season.append(storm)
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, "w", newline="") as file:
            file.write("date,time_utc,record,status,lat,lng,max_wind_kt,min_pressure_mb,34kt_wind_radius_nm_ne,34kt_wind_radius_nm_se,34kt_wind_radius_nm_nw,34kt_wind_radius_nm_sw,50kt_wind_radius_nm_ne,50kt_wind_radius_nm_se,50kt_wind_radius_nm_nw,50kt_wind_radius_nm_sw,64kt_wind_radius_nm_ne,64kt_wind_radius_nm_se,64kt_wind_radius_nm_nw,64kt_wind_radius_nm_sw,max_wind_radius_nm\n")
    else:
        with open(csv_path, "a", newline="") as file:
            file.write(line)