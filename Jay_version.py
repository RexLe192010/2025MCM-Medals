import pandas as pd
import csv
import os

def generate(data, filename):
    data_copy = data.copy()

    # change the order of columns
    new_order = ["Team", "Year", "Sport", "gold_medals", "silver_medals", "bronze_medals"]
    data_copy = data_copy[new_order]

    # sort the data by Team and Year, both ascending
    data_copy = data_copy.sort_values(by=["Team", "Year"], ascending=[True, True])
    print(data_copy.head())

    return data_copy


if __name__ == "__main__":
    # Load the gt5 data, which is the result after processing athletes.csv and hosts.csv
    lt5_df = pd.read_csv("processed/lt5_sports.csv")
    stable_df = pd.read_csv("processed/stable_sports.csv")
    unstable_df = pd.read_csv("processed/unstable_sports.csv")

    print(lt5_df.head())

    lt5_jay = generate(lt5_df, "lt5")
    stable_jay = generate(stable_df, "stable")
    unstable_jay = generate(unstable_df, "unstable")

    lt5_jay.to_csv("processed/lt5_sports_jay.csv", index=False)
    stable_jay.to_csv("processed/stable_sports_jay.csv", index=False)
    unstable_jay.to_csv("processed/unstable_sports_jay.csv", index=False)