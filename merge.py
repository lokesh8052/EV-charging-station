import json

with open("data.json") as f:
    stations = json.load(f)

with open("ev_usage_data.json") as f:
    usage = json.load(f)



# Create lookup table
station_map = {s["stationid"]: s for s in stations}

# Join data
joined_data = []

for u in usage:
    sid = u["stationid"]

    if sid in station_map:
        combined = {
            "stationid": sid,
            "city": station_map[sid]["city"],
            "state": station_map[sid]["state"],
            "date": u["date"],
            "hour": u["hour"],
            "sessions": u["sessions"],
            "energy_kwh": u["energy_kwh"]
        }
        joined_data.append(combined)

# print(joined_data[:5])
with open("mergeData.json","w") as f:
    json.dump(joined_data,f,indent=2)