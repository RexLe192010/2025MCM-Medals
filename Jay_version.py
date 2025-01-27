import pandas as pd
import csv
import os

def generate(data, filename):
    data_copy = data.copy()

    # change the order of columns
    new_order = ["Team", "Year", "Sport", "gold_medals", "silver_medals", "bronze_medals", "isHost"]
    data_copy = data_copy[new_order]

    # sort the data by Team and Year, both ascending
    data_copy = data_copy.sort_values(by=["Team", "Year"], ascending=[True, True])
    print(data_copy.head())

    return data_copy

def compute_stable_over_total_2024():
    # Load the data
    stable_data = pd.read_csv("processed/stable_sports.csv")
    athletes_data = pd.read_csv("raw/summerOly_athletes.csv")
    # in order to check the correctness, load data for unstable and lt5 sports
    unstable_data = pd.read_csv("processed/unstable_sports.csv")

    # filter out the data for 2024
    stable_2024 = stable_data[stable_data["Year"] == 2024]
    athletes_2024 = athletes_data[athletes_data["Year"] == 2024]

    stable_golds = 0
    unstable_golds = 0
    total_golds = 0

    stable_sports = set(stable_2024["Sport"].unique())

    # get the total number of medals for stable sports in 2024
    for sport in stable_2024["Sport"].unique():
        sport_data = stable_2024[stable_2024["Sport"] == sport]
        sport_total_medals = sport_data["sport_total_medals"].iloc[0]
        stable_golds += sport_total_medals
    
    for sport in unstable_data["Sport"].unique():
        sport_data = unstable_data[unstable_data["Sport"] == sport]
        sport_total_medals = sport_data["sport_total_medals"].iloc[0]
        unstable_golds += sport_total_medals
    
    # get the total number of medals for all sports in 2024
    total_golds = athletes_2024["Event"].nunique()

    print("Stable gold medals in 2024:", stable_golds / 3)
    print("Unstable gold medals in 2024:", unstable_golds / 3)
    print("Total gold medals in 2024:", total_golds)
    print("Stable sports:", stable_sports)

    ratio = (stable_golds / 3) / total_golds

    return ratio



if __name__ == "__main__":
    # Load the gt5 data, which is the result after processing athletes.csv and hosts.csv
    lt5_df = pd.read_csv("processed/lt5_sports.csv")
    stable_df = pd.read_csv("processed/stable_sports.csv")
    unstable_df = pd.read_csv("processed/unstable_sports.csv")

    print(lt5_df.head())

    # lt5_jay = generate(lt5_df, "lt5")
    # stable_jay = generate(stable_df, "stable")
    # unstable_jay = generate(unstable_df, "unstable")

    # lt5_jay.to_csv("processed/lt5_sports_jay.csv", index=False)
    # stable_jay.to_csv("processed/stable_sports_jay.csv", index=False)
    # unstable_jay.to_csv("processed/unstable_sports_jay.csv", index=False)


    # compute the ratio of stable gold medals to total gold medals in 2024
    ratio = compute_stable_over_total_2024()
    print("Ratio of stable gold medals to total gold medals in 2024:", ratio)