import json
import matplotlib.pyplot as plt

# better style
plt.style.use("dark_background")

# load data
with open("olap_results.json") as f:
    data = json.load(f)

city_count = data["city_count (stations)"]
hourly_usage = data["hourly_usage (sessions)"]
energy_per_hour = data["hourly_energy (kWh)"]
city_energy = data["city_energy (kWh)"]
top_city_energy = data["top_city_per_hour_energy"]

# prepare data
hours = sorted(map(int, hourly_usage.keys()))
sessions = [hourly_usage[str(h)] for h in hours]
energy_vals = [energy_per_hour[str(h)] for h in hours]

# city energy (top 10)
sorted_energy = sorted(city_energy.items(), key=lambda x: x[1], reverse=True)[:10]
cities_energy = [c for c, _ in sorted_energy]
energy_city_vals = [v for _, v in sorted_energy]

# top city energy per hour
top_energy = [top_city_energy[str(h)]["energy_kwh"] for h in hours]

# -----------------------------
# SUBPLOTS
# -----------------------------
fig, axs = plt.subplots(3, 2, figsize=(14, 12))

# 1️⃣ Stations per City (gradient feel)
axs[0, 0].bar(city_count.keys(), city_count.values(), color="cyan")
axs[0, 0].set_title("Stations per City", fontsize=12)
axs[0, 0].tick_params(axis='x', rotation=90)

# 2️⃣ Usage per Hour (neon line)
axs[0, 1].plot(hours, sessions, linewidth=2)
axs[0, 1].fill_between(hours, sessions, alpha=0.3)
axs[0, 1].set_title("Usage per Hour (Sessions)")
axs[0, 1].set_xlabel("Hour")
axs[0, 1].set_ylabel("Sessions")

# 3️⃣ Energy per Hour (highlight peak)
axs[1, 0].plot(hours, energy_vals, linewidth=2)
peak_idx = energy_vals.index(max(energy_vals))
axs[1, 0].scatter(hours[peak_idx], energy_vals[peak_idx], s=80)
axs[1, 0].set_title("Energy per Hour (kWh)")
axs[1, 0].set_xlabel("Hour")
axs[1, 0].set_ylabel("kWh")

# 4️⃣ City-wise Energy (top 10)
axs[1, 1].bar(cities_energy, energy_city_vals)
axs[1, 1].set_title("Top Cities by Energy")
axs[1, 1].tick_params(axis='x', rotation=45)

# 5️⃣ Top City Energy per Hour
axs[2, 0].plot(hours, top_energy, linewidth=2)
axs[2, 0].fill_between(hours, top_energy, alpha=0.3)
axs[2, 0].set_title("Top City Energy per Hour")
axs[2, 0].set_xlabel("Hour")
axs[2, 0].set_ylabel("kWh")

# remove empty plot
fig.delaxes(axs[2, 1])

plt.tight_layout()
plt.show()