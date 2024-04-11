import os
import csv
import json

year = ''
name = ''

with open('hurdat2.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    if 'AL' in line:
        if year != '' and name != '':
            with open(f"hurdat2CSV/{year}/{name}.csv", 'r', newline='') as file:
                data = list(csv.DictReader(file))
            with open(f"hurdat2JSON/{year}/{name}.json", 'w') as json_file:
                json.dump(data, json_file, indent=2)
        values = line.strip().split(',')
        if year != values[0][-4:]:
            i=0
        i+=1
        year = values[0][-4:]
        name = values[1].replace(" ", "")
        if name == "UNNAMED":
            name = f"{name}_{i}"
        if not os.path.exists(f"hurdat2CSV/{year}"):
            os.makedirs(f"hurdat2CSV/{year}")
        with open(f"hurdat2CSV/{year}/{name}.csv", 'w', newline='') as file:
            file.write("date,time_utc,record,status,lat,lng,max_wind_kt,min_pressure_mb,34kt_wind_radius_nm_ne,34kt_wind_radius_nm_se,34kt_wind_radius_nm_nw,34kt_wind_radius_nm_sw,50kt_wind_radius_nm_ne,50kt_wind_radius_nm_se,50kt_wind_radius_nm_nw,50kt_wind_radius_nm_sw,64kt_wind_radius_nm_ne,64kt_wind_radius_nm_se,64kt_wind_radius_nm_nw,64kt_wind_radius_nm_sw,max_wind_radius_nm\n")
        if not os.path.exists(f"hurdat2JSON/{year}"):
            os.makedirs(f"hurdat2JSON/{year}")
    else:
        with open(f"hurdat2CSV/{year}/{name}.csv", 'a', newline='') as file:
            file.write(line)