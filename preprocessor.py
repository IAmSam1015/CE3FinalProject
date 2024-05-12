import pandas as pd

df = pd.read_csv("Airbnb_Data.csv")

df = df.dropna()

df.to_csv("Cleaned.csv", index=False)
