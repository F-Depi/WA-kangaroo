import json
import pandas as pd
import matplotlib.pyplot as plt


# Let's get the dates of available rankings
with open('rankings_dates.json', 'r') as f:
    dates_json = json.load(f)
dates = []
for d in dates_json:
    dates.append(d["value"])
dates = dates[::-1]
dates = pd.to_datetime(dates)


def canguro(sex, event):
    df = pd.read_csv(f"data/{sex}_{event}/{sex}_{event}.csv")

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by=["Competitor", "DOB", "Country", "Date"])

    df["Prev Place"] = df.groupby(["Competitor", "DOB", "Country"])["Place"].shift(1)
    df["Prev Score"] = df.groupby(["Competitor", "DOB", "Country"])["Score"].shift(1)
    df["Prev Date"] = df.groupby(["Competitor", "DOB", "Country"])["Date"].shift(1)

    # Function to find previous date in Dates list
    def find_prev_date(date):
        prev = [d for d in dates if d < date]
        return prev[-1] if prev else pd.NaT

    mask = df["Prev Date"] == df["Date"].apply(find_prev_date)

    df.loc[mask, "Place diff"] = df["Place"] - df["Prev Place"]
    df.loc[mask, "Score diff"] = df["Score"] - df["Prev Score"]

    df = df.sort_values(by=["Place diff"])
    df.to_csv("canguro.csv", index=False)

sex = "women"
event = "long-jump"
#caguro(sex, event)

df = pd.read_csv("canguro.csv")
df = df.sort_values(by=["Place diff"])
df.to_csv("canguro.csv", index=False)
