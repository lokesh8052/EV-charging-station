import json
import random
from datetime import datetime, timedelta

# load station dataset
with open("data.json") as f:
    stations = json.load(f)

usage = []

start = datetime(2024,1,1)

for day in range(30):  # 30 days data
    date = start + timedelta(days=day)

    for station in stations:
        for hour in range(24):

            if 18 <= hour <= 22:     # peak evening
                sessions = random.randint(3,7)
            elif 7 <= hour <= 9:     # morning
                sessions = random.randint(2,5)
            else:
                sessions = random.randint(0,2)

            energy = sessions * random.uniform(10,25)

            usage.append({
                "stationid": station["stationid"],
                "date": date.strftime("%Y-%m-%d"),
                "hour": hour,
                "sessions": sessions,
                "energy_kwh": round(energy,2)
            })

with open("ev_usage_data.json","w") as f:
    json.dump(usage,f,indent=2)

print("Synthetic usage data generated!")