import pandas as pd

FLEXINDEX_FILE = "flexindex_28d_moving_average_24h_1mwh_1mw_100eff_1nc_100dd_0sesoc.csv"

ours = pd.read_csv("results_daily.csv")
flex = pd.read_csv(FLEXINDEX_FILE)
flex["date"] = flex["Unnamed: 0"].str[:10]

flex_days = flex[flex["date"] >= "2025-10-01"].drop_duplicates("date")
ours = ours[ours["date"].isin(flex_days["date"])].copy()
ours["moving_avg_28"] = ours["revenue_hourly"].rolling(28).mean()

compare = ours.merge(flex_days[["date", "DA Auction Revenue"]], on="date")
compare = compare[compare["date"] >= "2025-11-15"]
compare["difference"] = compare["moving_avg_28"] - compare["DA Auction Revenue"]

print(compare[["date", "moving_avg_28", "DA Auction Revenue", "difference"]].head())
print("Rows compared:", len(compare))
print("Max absolute difference:", round(compare["difference"].abs().max(), 4), "EUR per day")
