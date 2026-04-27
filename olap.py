import json

# load data
with open("cleaned_dimension.json") as f:
    stations = json.load(f)

with open("fact_table.json") as f:
    usage = json.load(f)

# lookup
station_map = {s["stationid"]: s for s in stations}

# -------------------------
# OLAP 1: Stations per City
# -------------------------
city_count = {}
for s in stations:
    city = s["city"]
    city_count[city] = city_count.get(city, 0) + 1

# -------------------------
# OLAP 2: Usage per Hour
# -------------------------
hourly_usage = {}
for u in usage:
    h = u["hour"]
    hourly_usage[h] = hourly_usage.get(h, 0) + u["sessions"]

# -------------------------
# OLAP 3: City-wise Usage
# -------------------------
city_usage = {}
for u in usage:
    sid = str(u["stationid"])
    if sid in station_map:
        city = station_map[sid]["city"]
        city_usage[city] = city_usage.get(city, 0) + u["sessions"]

# -------------------------
# OLAP 4: Peak Hour
# -------------------------
peak_hour = max(hourly_usage, key=hourly_usage.get)

# print results
print("Stations per city:", city_count)
print("Hourly usage:", hourly_usage)
print("City-wise usage:", city_usage)
print("Peak hour:", peak_hour)

# save results
result = {
    "city_count": city_count,
    "hourly_usage": hourly_usage,
    "city_usage": city_usage,
    "peak_hour": peak_hour
}

with open("olap_results.json", "w") as f:
    json.dump(result, f, indent=2)

print("\nOLAP results saved!")