import os

year = ''
name = ''
i=0

with open('hurdat2.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    if 'AL' in line:
        i+=1
        values = line.strip().split(',')
        year = values[0][-4:]
        name = values[1].replace(" ", "")
        if name == "UNNAMED":
            name = f"{name}_{i}"
        if not os.path.exists(f"hurdat2/{year}"):
            os.makedirs(f"hurdat2/{year}")
        with open(f"hurdat2/{year}/{name}.csv", 'w', newline='') as file:
            file.write("date,time_utc,record,status,lat,lng,max_wind_kt,min_pressure_mb,34kt_wind_radius_nm_ne,34kt_wind_radius_nm_se,34kt_wind_radius_nm_nw,34kt_wind_radius_nm_sw,50kt_wind_radius_nm_ne,50kt_wind_radius_nm_se,50kt_wind_radius_nm_nw,50kt_wind_radius_nm_sw,64kt_wind_radius_nm_ne,64kt_wind_radius_nm_se,64kt_wind_radius_nm_nw,64kt_wind_radius_nm_sw,max_wind_radius_nm\n")
    else:
        with open(f"hurdat2/{year}/{name}.csv", 'a', newline='') as file:
            file.write(line)