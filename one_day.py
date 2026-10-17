import pandas as pd
from optimizer import optimizer

# one test day and the battery like the FlexIndex reference: 1 MWh, 1 MW, 1 cycle per day
DAY = "2025-10-01"
ENERGY_CAP = 1  # MWh
POWER_CAP = 1   # MW
N_CYCLES = 1

# load the prices and keep only the 96 quarter-hours of the test day
prices = pd.read_csv("prices_de_lu_15min.csv")
day = prices[prices["timestamp"].str.startswith(DAY)]
price_list = day["price_eur_mwh"].tolist()
times = day["timestamp"].str[11:16].tolist()
print("Quarter-hours:", len(price_list), "| min price:", min(price_list), "| max price:", max(price_list))

# optimize the day with the original model (hourly blocks), None because HiGHS needs no solver path
opt = optimizer(None)
soc, cha, dis, profit = opt.step1_optimize_daa(
    n_cycles=N_CYCLES, energy_cap=ENERGY_CAP, power_cap=POWER_CAP, daa_price_vector=price_list)

# print every quarter-hour where the battery charges or discharges, to check if it makes sense
for q in range(96):
    if cha[q] > 0.001:
        print(times[q], "charge   ", round(POWER_CAP / 4 * cha[q], 3), "MWh at", price_list[q], "EUR/MWh")
    if dis[q] > 0.001:
        print(times[q], "discharge", round(POWER_CAP / 4 * dis[q], 3), "MWh at", price_list[q], "EUR/MWh")

print("Max state of charge:", round(max(soc), 3), "MWh")
print("Revenue:", round(profit, 2), "EUR")
