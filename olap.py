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
# OLAP 2: Usage per Hour (sessions + energy)
# -------------------------
hourly_usage = {}        # sessions
energy_per_hour = {}     # kWh

hour_city_sessions = {}  # hour -> city -> sessions
hour_city_energy = {}    # hour -> city -> energy

for u in usage:
    hour = u["hour"]
    sid = str(u["stationid"])
    sessions = u["sessions"]
    energy = u["energy_kwh"]

    # total per hour
    hourly_usage[hour] = hourly_usage.get(hour, 0) + sessions
    energy_per_hour[hour] = energy_per_hour.get(hour, 0) + energy

    if sid in station_map:
        city = station_map[sid]["city"]

        # sessions per city per hour
        if hour not in hour_city_sessions:
            hour_city_sessions[hour] = {}
        hour_city_sessions[hour][city] = hour_city_sessions[hour].get(city, 0) + sessions

        # energy per city per hour
        if hour not in hour_city_energy:
            hour_city_energy[hour] = {}
        hour_city_energy[hour][city] = hour_city_energy[hour].get(city, 0) + energy

# -------------------------
# OLAP 3: Top City per Hour
# -------------------------
hour_top_city_sessions = {}
hour_top_city_energy = {}

for hour in hour_city_sessions:
    # sessions
    top_city_s = max(hour_city_sessions[hour], key=hour_city_sessions[hour].get)
    hour_top_city_sessions[hour] = {
        "city": top_city_s,
        "sessions": hour_city_sessions[hour][top_city_s]
    }

    # energy
    top_city_e = max(hour_city_energy[hour], key=hour_city_energy[hour].get)
    hour_top_city_energy[hour] = {
        "city": top_city_e,
        "energy_kwh": round(hour_city_energy[hour][top_city_e], 2)
    }

# -------------------------
# OLAP 4: City-wise totals
# -------------------------
city_usage = {}
city_energy = {}

for u in usage:
    sid = str(u["stationid"])
    if sid in station_map:
        city = station_map[sid]["city"]

        city_usage[city] = city_usage.get(city, 0) + u["sessions"]
        city_energy[city] = city_energy.get(city, 0) + u["energy_kwh"]

# -------------------------
# OLAP 5: Peak Hours
# -------------------------
peak_hour_sessions = max(hourly_usage, key=hourly_usage.get)
peak_hour_energy = max(energy_per_hour, key=energy_per_hour.get)

# -------------------------
# PRINT RESULTS WITH UNITS
# -------------------------
print("\nStations per City (count):")
print(city_count)

print("\nHourly Usage (sessions):")
print(hourly_usage)

print("\nHourly Energy (kWh):")
print(energy_per_hour)

print("\nTop City per Hour (sessions):")
for h in sorted(hour_top_city_sessions):
    print(f"Hour {h}: {hour_top_city_sessions[h]['city']} ({hour_top_city_sessions[h]['sessions']} sessions)")

print("\nTop City per Hour (energy kWh):")
for h in sorted(hour_top_city_energy):
    print(f"Hour {h}: {hour_top_city_energy[h]['city']} ({hour_top_city_energy[h]['energy_kwh']} kWh)")

print("\nCity-wise Usage (sessions):")
print(city_usage)

print("\nCity-wise Energy (kWh):")
print(city_energy)

print("\nPeak Hour (sessions):", peak_hour_sessions)
print("Peak Hour (energy):", peak_hour_energy)

# -------------------------
# SAVE RESULTS
# -------------------------
result = {
    "city_count (stations)": city_count,
    "hourly_usage (sessions)": hourly_usage,
    "hourly_energy (kWh)": energy_per_hour,
    "top_city_per_hour_sessions": hour_top_city_sessions,
    "top_city_per_hour_energy": hour_top_city_energy,
    "city_usage (sessions)": city_usage,
    "city_energy (kWh)": city_energy,
    "peak_hour_sessions": peak_hour_sessions,
    "peak_hour_energy": peak_hour_energy
}

with open("olap_results.json", "w") as f:
    json.dump(result, f, indent=2)

print("\nOLAP results saved!")