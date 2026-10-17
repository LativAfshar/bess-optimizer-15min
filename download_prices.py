# Data: Bundesnetzagentur | SMARD.de (CC BY 4.0), retrieved via api.energy-charts.info (Fraunhofer ISE)

# import libraries: urllib for the request, json to read the answer, csv to write the file
import csv
import json
import urllib.request

# we pull the prices from this URL and save them in OUTFILE
URL = "https://api.energy-charts.info/v2/price?bzn=DE-LU&start=2025-10-01&end=2026-09-30"
OUTFILE = "prices_de_lu_15min.csv"

# here the real pulling of the data from the API happens, the JSON answer becomes a Python dictionary
with urllib.request.urlopen(URL, timeout=120) as response:
    data = json.load(response)

# print resolution and unit and check that it is 15 minutes, otherwise error
print("Resolution:", data["resolution"], "| Unit:", data["unit"])
print("License:", data["license"])
if data["resolution"] != "PT15M":
    raise ValueError("Expected 15-minute prices, got " + data["resolution"])

# write the data into the CSV: one row per quarter-hour with timestamp and price
with open(OUTFILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "price_eur_mwh"])
    for row in data["data"]:
        writer.writerow([row["timestamp"], row["values"]["day_ahead_price"]])

# print how many rows were saved in the CSV
print("Saved", len(data["data"]), "rows to", OUTFILE)
