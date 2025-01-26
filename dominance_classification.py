import pandas as pd
import csv
import os

def compute_dominance(data):
    result = {}
    dominant_count = 0
    dominant = set()
    errors = set()
    length = len(data["Sport"].unique())

    for discipline in data["Sport"].unique():
        print(discipline)
        # data should be the csv file read in main, as a pandas dataframe
        # filter out some rows
        filtered_data = data[data["Sport"] == discipline]
        filtered_data = filtered_data[data["Year"] >= 2016]

        filtered_data = filtered_data[["Team", "Year", "Medal"]]
        # print(filtered_data.head())
        candidates = set(filtered_data["Team"].unique())

        # iterate over different years
        for year in filtered_data["Year"].unique(): # should be 2016, 2020, 2024
            print(year)
            print(candidates)
            if len(candidates) == 0:
                result[discipline] = False
            year_data = filtered_data[filtered_data["Year"] == year]
            # compute the total number of medals for this discipline in this year
            total_golds = 0
            for medal in year_data["Medal"]:
                if medal == "Gold":
                    total_golds += 1
            print(total_golds)
            # iterate over different teams to compute their 
            for team in filtered_data["Team"].unique():
                if team not in candidates:
                    continue
                team_data = year_data[year_data["Team"] == team]
                # compute the number of gold medals for this team in this year
                team_golds = 0
                for medal in team_data["Medal"]:
                    if medal == "Gold":
                        team_golds += 1
                # compute the dominance of this team in this year
                if total_golds == 0:
                    errors.add(discipline)
                    continue
                else:
                    dominance = team_golds / total_golds
                    if dominance < 0.6:
                        candidates.remove(team)

        if len(candidates) == 0:
            result[discipline] = False
        else:
            dominant_count += 1
            dominant.add(discipline)
            result[discipline] = True

    print("Total disciplines:", length)
    print("Dominant disciplines:", dominant)      
    print("Dominant count:", dominant_count)
    print("Disciplines with errors:", errors)
    return result
    



if __name__ == "__main__":
    # Load the data
    data = pd.read_csv("raw/summerOly_athletes.csv")
    # Display the first 5 rows
    print(data.head())

    result = compute_dominance(data)
    print(result)