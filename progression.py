import pandas as pd
import matplotlib.pyplot as plt

sex = "women"
event = "long-jump"
competitor = "Giulia RICCARDI"

df = pd.read_csv(f"data/{sex}_{event}.csv")
df_giulia = df[df["Competitor"] == competitor].sort_values(by=["Date"])

# Make sure 'date' is datetime
df_giulia["date"] = pd.to_datetime(df_giulia["Date"])

scale = 300 
plt.figure(figsize=(1920 / scale, 1080 / scale))
plt.plot(df_giulia["Date"], df_giulia["Place"], 'o-')
plt.xlabel("Data")
plt.ylabel("Ranking Mondiale")
plt.title(f"Progressione nel Ranking Mondiale di {competitor}")

# Rotate x-axis labels
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.grid()
plt.savefig(f"figures/{competitor}_{event}.png", dpi=scale)
plt.show()

