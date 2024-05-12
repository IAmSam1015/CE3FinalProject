import pandas as pd

file = "Airbnb_Data.csv"
data = pd.read_csv(
    file, header=0
)  # Explicitly specify that the first row (0-indexed) is the header
