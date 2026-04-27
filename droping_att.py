import json

# fields to KEEP
keep_fields = {
    "stationid",
    "name",
    "city",
    "state",
    "lattitude",   # will rename later if needed
    "latitude",
    "longitude",
    "availability",
    "pricing"
}

with open("data.json") as f:
    data = json.load(f)

cleaned = []

for s in data:
    new_obj = {}

    for k in keep_fields:
        if k in s:
            new_obj[k] = s[k]

    cleaned.append(new_obj)

# save result
with open("filtered_data.json", "w") as f:
    json.dump(cleaned, f, indent=2)

print("Unwanted columns removed!")