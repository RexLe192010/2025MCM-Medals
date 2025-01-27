import pandas as pd
import csv
import os

# in this file, I need to extend the stable_sports data to include countries that do not participate in the Olympics


def get_countries(data):
    # get all the countries that have participated in the Olympics
    countries = data["Team"].unique()
    return countries


def add_NA(data, countries):
    # get the copy of the data
    data_copy = data.copy()
    new_rows = []

    # add more rows to the data to include countries that do not participate in the Olympics
    for sport in data_copy["Sport"].unique():
        sport_data = data_copy[data_copy["Sport"] == sport]
        for year in sport_data["Year"].unique():
            year_data = sport_data[sport_data["Year"] == year]

            # get the total medals and participants for this sport in this year
            sport_total_medals = year_data["sport_total_medals"].iloc[0]
            sport_total_participants = year_data["sport_total_participants"].iloc[0]

            for country in countries:
                if country not in year_data["Team"].unique():
                    new_row = {
                        "Sport": sport, 
                        "Year": year, 
                        "Team": country, 
                        "gold_medals": "NA", 
                        "silver_medals": "NA", 
                        "bronze_medals": "NA", 
                        "total_medals": "NA", 
                        "participants": "NA", 
                        "sport_total_medals": sport_total_medals, 
                        "sport_total_participants": sport_total_participants,
                        "isHost": 0
                        }
                    new_rows.append(new_row)

    new_rows_df = pd.DataFrame(new_rows)
    extended_data = pd.concat([data_copy, new_rows_df], ignore_index=True)

    # sort the data by Team and Year, both ascending
    extended_data = extended_data.sort_values(by=["Sport", "Year"], ascending=[True, True])

    return extended_data

if __name__ == "__main__":
    # Load the data
    stable_data = pd.read_csv("processed/stable_sports.csv")
    athletes_data = pd.read_csv("processed/summerOly_athletes_cleaned.csv")

    # get all the countries that have participated in the Olympics
    countries = get_countries(athletes_data)

    # add NA rows to the stable data
    extended_stable_data = add_NA(stable_data, countries)

    # write the extended stable data to a csv file
    extended_stable_data.to_csv("processed/extended_stable_sports.csv", index=False)