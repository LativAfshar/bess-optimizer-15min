import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv("results_daily.csv")
results["month"] = results["date"].str[:7]
monthly = results.groupby("month")[["revenue_hourly", "revenue_15min"]].sum()
monthly["difference_pct"] = (monthly["revenue_15min"] / monthly["revenue_hourly"] - 1) * 100
print(monthly.round(1))

x = np.arange(len(monthly))
width = 0.38
fig, ax = plt.subplots(figsize=(10, 5), facecolor="#fcfcfb")
ax.set_facecolor("#fcfcfb")
ax.bar(x - width / 2 - 0.01, monthly["revenue_hourly"], width, color="#2a78d6", label="Hourly blocks (like FlexIndex)")
ax.bar(x + width / 2 + 0.01, monthly["revenue_15min"], width, color="#eb6834", label="15 min")

for i in range(len(monthly)):
    ax.text(x[i], monthly["revenue_15min"].iloc[i] + 60, "+" + str(round(monthly["difference_pct"].iloc[i])) + "%",
            ha="center", fontsize=9, color="#52514e")

ax.set_ylim(0, monthly["revenue_15min"].max() * 1.08)
ax.set_xticks(x)
ax.set_xticklabels(pd.to_datetime(monthly.index).strftime("%b %y"))
ax.set_ylabel("Revenue (EUR per MW per month)", color="#52514e")
ax.set_title("Day-ahead revenue per month, 1 MW / 1 MWh battery, 1 cycle per day (DE-LU, Oct 2025 - Sep 2026)",
             loc="left", fontsize=11, color="#0b0b0b")
ax.legend(frameon=False, loc="upper left")
ax.grid(axis="y", color="#e5e4e0", linewidth=0.8)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(colors="#52514e")

fig.tight_layout()
fig.savefig("monthly_revenue.png", dpi=150)
print("Saved monthly_revenue.png")
