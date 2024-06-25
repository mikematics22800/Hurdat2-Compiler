import os
import csv
import json

year = ""
name = ""
years = []

with open("hurdat2.txt", "r") as file:
    lines = file.readlines()
    
for line in lines:
    if "AL" in line:
        values = line.strip().split(",")
        if year != "" and name != "":
            with open(f"hurdat2CSV/{year}/{name}.csv", "r", newline="") as file:
                csv_data=[]
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
                                if value.isdigit() or value[1:].isdigit():
                                    row[key] = int(value)
                                else: 
                                    row[key] = value
                            else:
                                row[key] = value
                    csv_data.append(row)
            with open(f"hurdat2JSON/{year}/{name}.json", "w") as file:
                json.dump(csv_data, file, indent=2)
            with open(f"hurdat2JSON/{year}/{name}.json", "r") as file:
                json_data = json.load(file)
            if 'Unnamed' in name:
                name = 'Unnamed' 
            json_data.insert(0, {
                "id": f"{values[0]}_{name}",
                "image": "",
                "fatalaties": 0,
                "cost_usd": 0,
                "retired": "false"
            })
            with open(f"hurdat2JSON/{year}/{name}.json", "w") as file:
                json.dump(json_data, file, indent=2)
            if year != values[0][-4:]:
                years.append(year)
                with open(f"hurdat2JSON/{year}/index.js", "w") as file:
                    for name in names:
                        file.write(f"import {name} from './{name}'\n")
                    file.write('\n')
                    file.write(f"const hurdat2_{year} = [\n")
                    for name in names:                         
                        file.write(f"   {name},\n")
                    file.write(']\n')
                    file.write('\n')
                    file.write(f"export default hurdat2_{year}")
        if year != values[0][-4:]:
            i=0
            names = []
        year = values[0][-4:]
        name = values[1].replace(" ", "")
        if name == "UNNAMED":
            i+=1
            name = f"{name}_{i}"
        name = name[0] + name[1:].lower()
        if "-" in name:
            name = name.replace("-", "_")
        names.append(name)
        with open(f"hurdat2CSV/{year}/{name}.csv", "w", newline="") as file:
            file.write("date,time_utc,record,status,lat,lng,max_wind_kt,min_pressure_mb,34kt_wind_radius_nm_ne,34kt_wind_radius_nm_se,34kt_wind_radius_nm_nw,34kt_wind_radius_nm_sw,50kt_wind_radius_nm_ne,50kt_wind_radius_nm_se,50kt_wind_radius_nm_nw,50kt_wind_radius_nm_sw,64kt_wind_radius_nm_ne,64kt_wind_radius_nm_se,64kt_wind_radius_nm_nw,64kt_wind_radius_nm_sw,max_wind_radius_nm\n")
    else:
        with open(f"hurdat2CSV/{year}/{name}.csv", "a", newline="") as file:
            file.write(line)

with open(f"hurdat2JSON/index.js", "w") as file:
    for year in years:
        file.write(f"import hurdat2_{year} from './{year}'\n")
    file.write('\n')
    file.write(f"const hurdat2 = [\n")
    for year in years:
        file.write(f"   hurdat2_{year},\n")
    file.write(']\n')
    file.write('\n')
    file.write('export default hurdat2')