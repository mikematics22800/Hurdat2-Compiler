import csv
import json
import os

with open("hurdat2.txt", "r") as file:
    lines = file.readlines()
    
year = 1851
years = []
names = []
number = 0

for line in lines:
    values = line.strip().split(",")
    if len(values) == 4:
        if len(names) > 0: 
            csv_data=[]
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
                    csv_data.append(row)
            json_path = f"hurdat2JSON/{year}/{name}.json"
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, "w") as file:
                json.dump(csv_data, file, indent=2)
            with open(json_path, "r") as file:
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
            with open(json_path, "w") as file:
                json.dump(json_data, file, indent=2)
            if year < int(values[0][-4:]):
                index_path = f"hurdat2JSON/{year}/index.js"
                os.makedirs(os.path.dirname(index_path), exist_ok=True)
                with open(index_path, "w") as file:
                    for name in names:
                        file.write(f"import {name} from './{name}'\n")
                    file.write('\n')
                    file.write(f"const hurdat2_{year} = [\n")
                    for name in names:                         
                        file.write(f"   {name},\n")
                    file.write(']\n')
                    file.write('\n')
                    file.write(f"export default hurdat2_{year}")
                years.append(year)
                year+=1
                names = []  
                number = 0
        name = values[1].replace(" ", "")
        if name == "UNNAMED":
            number+=1
            name = f"Unnamed_{number}"
        name = name[0] + name[1:].lower()
        name = name.replace("-", "_")
        names.append(name)
        csv_path = f"hurdat2CSV/{year}/{name}.csv"
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, "w", newline="") as file:
            file.write("date,time_utc,record,status,lat,lng,max_wind_kt,min_pressure_mb,34kt_wind_radius_nm_ne,34kt_wind_radius_nm_se,34kt_wind_radius_nm_nw,34kt_wind_radius_nm_sw,50kt_wind_radius_nm_ne,50kt_wind_radius_nm_se,50kt_wind_radius_nm_nw,50kt_wind_radius_nm_sw,64kt_wind_radius_nm_ne,64kt_wind_radius_nm_se,64kt_wind_radius_nm_nw,64kt_wind_radius_nm_sw,max_wind_radius_nm\n")
    else:
        with open(csv_path, "a", newline="") as file:
            file.write(line)

index_path = f"hurdat2JSON/index.js"
os.makedirs(os.path.dirname(index_path), exist_ok=True)
with open(index_path, "w") as file:
    for year in years:
        file.write(f"import hurdat2_{year} from './{year}'\n")
    file.write('\n')
    file.write(f"const hurdat2 = [\n")
    for year in years:
        file.write(f"   hurdat2_{year},\n")
    file.write(']\n')
    file.write('\n')
    file.write('export default hurdat2')
