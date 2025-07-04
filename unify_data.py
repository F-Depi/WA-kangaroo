import os
import pandas as pd


def unify_rankings_for_event(sex, event):
    df = pd.DataFrame()
    for file in os.listdir(f"data/{sex}_{event}/"):

        # Must be a file with sex_event_date
        if file.count("_") != 2 and file.startswith(f"{sex}_{event}"):
            continue

        df_date = pd.read_csv(f"data/{sex}_{event}/{file}")
        df_date = df_date.rename(columns={"Unnamed: 3": "Country"})
        df_date["Date"] = file[-14:-4]
        df = pd.concat([df, df_date])

    df["Event List"] = event.replace("-", " ").title()
    df.to_csv(f"data/{sex}_{event}/{sex}_{event}.csv", index=False)

sex = "women"
event = "long-jump"
#unify_rankings_for_event(sex, event)

sex = "men"
event = "110mh"
unify_rankings_for_event(sex, event)
