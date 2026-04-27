import json

with open("dimension_table.json") as f:
    data = json.load(f)

cleaned = []
seen = set()

# -----------------------------
# 2️⃣ CLEAN DIMENSION TABLE
# -----------------------------
for s in data:
    try:
        lat_val = s.get("latitude") or s.get("lattitude")
        lon_val = s.get("longitude")

        if lat_val in [None, "NA"] or lon_val in [None, "NA"]:
            continue

        lat = float(lat_val)
        lon = float(lon_val)

        availability = int(s.get("availability", 0))

        pricing_raw = s.get("pricing", 0)
        pricing = 0 if str(pricing_raw).lower() == "free" else pricing_raw

        name = s.get("name", "").replace("\u00a0", "").strip()

        # remove duplicates
        key = (name, lat, lon)
        if key in seen:
            continue
        seen.add(key)

        cleaned.append({
            "stationid": str(s.get("stationid")),
            "name": name,
            "city": s.get("city", "").strip(),
            "state": s.get("state", "").strip(),
            "latitude": lat,
            "longitude": lon,
            "availability": availability,
            "pricing": pricing
        })

    except:
        continue

# save cleaned dimension table
with open("cleaned_dimension.json", "w") as f:
    json.dump(cleaned, f, indent=2)

print("Cleaned rows:", len(cleaned))