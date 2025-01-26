import pandas as pd
import csv
import os


# This file is to generate a dataframe that has the first 5 Olympics data for each gt5 sport
def generate(data):
    result = []
    for sport in data["Sport"].unique():
        sport_data = data[data["Sport"] == sport]

        # need the data from most recent 5 years
        years = sorted(sport_data["Year"].unique())[:5]
        for year in years:
            year_data = sport_data[sport_data["Year"] == year]
            result.append(year_data)
    
    # convert the list of dataframes to a single dataframe
    result_df = pd.concat(result, ignore_index=True)
    return result_df


if __name__ == "__main__":
    # Load the data
    gt5_data = pd.read_csv("gt5_sports.csv")
    print(gt5_data.head())

    gt5_f5_data = generate(gt5_data)

    # write the data to a new file
    gt5_f5_data.to_csv("gt5_f5.csv", index=False)