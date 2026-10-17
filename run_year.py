import pandas as pd
from optimizer import optimizer

# battery like the FlexIndex reference: max energy 1 MWh, max power 1 MW, 1 cycle per day
ENERGY_CAP = 1  # MWh
POWER_CAP = 1   # MW
N_CYCLES = 1

# load the prices, date = first 10 characters of the timestamp, so we can group by day
prices = pd.read_csv("prices_de_lu_15min.csv")
prices["date"] = prices["timestamp"].str[:10]

# None because HiGHS needs no solver path
opt = optimizer(None)
results = []

# go through the year day by day, skip the two clock change days (92 and 100 quarter-hours),
# because the model only works with 96
for date, day in prices.groupby("date"):
    price_list = day["price_eur_mwh"].tolist()
    if len(price_list) != 96:
        print("Skipped", date, "with", len(price_list), "quarter-hours")
        continue
    # optimize the same day twice: with hourly blocks (original) and with free 15-min positions
    soc, cha, dis, profit_hourly = opt.step1_optimize_daa(
        n_cycles=N_CYCLES, energy_cap=ENERGY_CAP, power_cap=POWER_CAP, daa_price_vector=price_list,
        hourly_blocks=True)
    soc, cha, dis, profit_15min = opt.step1_optimize_daa(
        n_cycles=N_CYCLES, energy_cap=ENERGY_CAP, power_cap=POWER_CAP, daa_price_vector=price_list,
        hourly_blocks=False)
    results.append({"date": date, "revenue_hourly": profit_hourly, "revenue_15min": profit_15min})

# save the results as CSV and print them, annualised = mean per day * 365 because 2 days are missing
results = pd.DataFrame(results)
results.to_csv("results_daily.csv", index=False)

hourly_year = results["revenue_hourly"].mean() * 365
min15_year = results["revenue_15min"].mean() * 365

print("Days:", len(results))
print("Hourly blocks (mean * 365):", round(hourly_year), "EUR/MW/year")
print("15 min (mean * 365):       ", round(min15_year), "EUR/MW/year")
print("Difference:", round(min15_year - hourly_year), "EUR/MW/year =", round((min15_year / hourly_year - 1) * 100, 1), "%")
# check: 15 min should never be worse than hourly blocks (small tolerance for solver rounding)
print("Days where 15 min is worse:", (results["revenue_15min"] < results["revenue_hourly"] - 0.000001).sum())
