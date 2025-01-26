import pandas as pd
import csv
import os

def compute_dominance(data):
    # should be run before the last classification criterion
    dominant = set()
    non_dominant = set()

    # filter out rows with year less than 2016
    filtered_data = data[data["Year"] >= 2016]

    for sport in filtered_data["Sport"].unique():
        # print(sport)
        # data should be the csv file read in main, as a pandas dataframe
        # filter out some rows
        sport_data = filtered_data[filtered_data["Sport"] == sport]
        candidates = set(sport_data["Team"].unique())

        # iterate over different years
        for year in sport_data["Year"].unique(): # should be 2016, 2020, 2024
            total_golds = sport_data["sport_total_medals"].iloc[0] / 3
            # print(total_golds)
            year_data = sport_data[sport_data["Year"] == year]
            
            # iterate over different teams to check their dominance
            for team in filtered_data["Team"].unique():
                if team not in candidates:
                    continue
                team_data = year_data[year_data["Team"] == team]
                # print(team_data.head())

                # filter out empty dataframes
                if team_data.empty:
                    continue

                # compute the number of gold medals for this team in this year
                team_golds = team_data["gold_medals"].iloc[0]

                # compute the dominance of this team in this year
                dominance = team_golds / total_golds
                if dominance < 0.6:
                    candidates.remove(team)

        if len(candidates) == 0:
            non_dominant.add(sport)
        else:
            dominant.add(sport)

    print("Dominant disciplines:", dominant)
    print("Non-dominant disciplines:", non_dominant)

    # extract dominant and non-dominant disciplines from the original data (instead of the filtered data)
    dominant_df = data[data["Sport"].isin(dominant)]
    non_dominant_df = data[data["Sport"].isin(non_dominant)]

    # write the results to a csv file
    dominant_df.to_csv("processed/dominant_disciplines.csv", index=False)
    non_dominant_df.to_csv("processed/non_dominant_disciplines.csv", index=False)

    return dominant_df, non_dominant_df


def compute_turnover(non_dominant_df):
    turnovers = []

    # filter data for the most recent 6 olympic games
    filtered_data = non_dominant_df[non_dominant_df["Year"] >= 2004]

    # iterate over different sports
    for sport in filtered_data["Sport"].unique():
        current_turnover = 0
        sport_data = filtered_data[filtered_data["Sport"] == sport]

        # iterate over different teams/countries
        for team in sport_data["Team"].unique():
            team_data = sport_data[sport_data["Team"] == team]
            print(team_data.head())

            if team_data.empty:
                continue

            # extract the data for each year
            team_data_2024 = team_data[team_data["Year"] == 2024]
            team_data_2020 = team_data[team_data["Year"] == 2020]
            team_data_2016 = team_data[team_data["Year"] == 2016]
            team_data_2012 = team_data[team_data["Year"] == 2012]
            team_data_2008 = team_data[team_data["Year"] == 2008]
            team_data_2004 = team_data[team_data["Year"] == 2004]

            if team_data_2024.empty or team_data_2020.empty or team_data_2016.empty or team_data_2012.empty or team_data_2008.empty or team_data_2004.empty:
                continue

            # compute the total number of gold medals for this sport in each year
            total_golds_2024 = team_data_2024["sport_total_medals"].iloc[0] / 3
            total_golds_2020 = team_data_2020["sport_total_medals"].iloc[0] / 3
            total_golds_2016 = team_data_2016["sport_total_medals"].iloc[0] / 3
            total_golds_2012 = team_data_2012["sport_total_medals"].iloc[0] / 3
            total_golds_2008 = team_data_2008["sport_total_medals"].iloc[0] / 3
            total_golds_2004 = team_data_2004["sport_total_medals"].iloc[0] / 3

            # compute the dominance of this team in each year
            dominance_2024 = team_data_2024["gold_medals"].iloc[0] / total_golds_2024
            dominance_2020 = team_data_2020["gold_medals"].iloc[0] / total_golds_2020
            dominance_2016 = team_data_2016["gold_medals"].iloc[0] / total_golds_2016
            dominance_2012 = team_data_2012["gold_medals"].iloc[0] / total_golds_2012
            dominance_2008 = team_data_2008["gold_medals"].iloc[0] / total_golds_2008
            dominance_2004 = team_data_2004["gold_medals"].iloc[0] / total_golds_2004

            to2024 = abs(dominance_2024 - dominance_2020)
            to2020 = abs(dominance_2020 - dominance_2016)
            to2016 = abs(dominance_2016 - dominance_2012)
            to2012 = abs(dominance_2012 - dominance_2008)
            to2008 = abs(dominance_2008 - dominance_2004)

            # compute the turnover for this team in each year
            # to2024 = team_data_2024["gold_medals"].iloc[0] / total_golds_2024 - team_data_2020["gold_medals"].iloc[0] / total_golds_2020
            # to2020 = team_data_2020["gold_medals"].iloc[0] / team_data_2020["sport_total_medals"] - team_data_2016["gold_medals"].iloc[0] / team_data_2016["sport_total_medals"]
            # to2016 = team_data_2016["gold_medals"].iloc[0] / team_data_2016["sport_total_medals"] - team_data_2012["gold_medals"].iloc[0] / team_data_2012["sport_total_medals"]
            # to2012 = team_data_2012["gold_medals"].iloc[0] / team_data_2012["sport_total_medals"] - team_data_2008["gold_medals"].iloc[0] / team_data_2008["sport_total_medals"]
            # to2008 = team_data_2008["gold_medals"].iloc[0] / team_data_2008["sport_total_medals"] - team_data_2004["gold_medals"].iloc[0] / team_data_2004["sport_total_medals"]

            # compute the overall turnover for this team in this sport
            current_turnover += 0.411 * to2024 + 0.259 * to2020 + 0.163 * to2016 + 0.103 * to2012 + 0.065 * to2008
        
        turnovers.append((sport, current_turnover))
    

    # sort the turnovers in descending order
    turnovers.sort(key=lambda x: x[1])
    print(turnovers)

    stable_sports = []
    unstable_sports = []

    # the first half will be considered stable, and the second half will be considered unstable
    for i in range(len(turnovers)):
        if i < len(turnovers) / 2:
            stable_sports.append(turnovers[i][0])
        else:
            unstable_sports.append(turnovers[i][0])
    print("Stable disciplines:", stable_sports)
    print("Unstable disciplines:", unstable_sports)

    # extract stable and unstable sports from the original data
    stable_df = non_dominant_df[non_dominant_df["Sport"].isin(stable_sports)]
    unstable_df = non_dominant_df[non_dominant_df["Sport"].isin(unstable_sports)]

    return stable_df, unstable_df
    



if __name__ == "__main__":
    # Load the gt5 data, which is the result after processing athletes.csv and hosts.csv
    data = pd.read_csv("processed/gt5_sports.csv")
    # Display the first 5 rows
    print(data.head())

    # classify the sports into dominant and non-dominant disciplines
    dominant_df, non_dominant_df = compute_dominance(data)

    # classify the non-dominant disciplines into stable and unstable sports
    stable_df, unstable_df = compute_turnover(non_dominant_df)

    # finallly, merge the dominant and stable sports into a single dataframe
    final_stable_df = pd.concat([dominant_df, stable_df])
    final_unstable_df = unstable_df

    # write the final results to a csv file
    final_stable_df.to_csv("processed/stable_sports.csv", index=False)
    final_unstable_df.to_csv("processed/unstable_sports.csv", index=False)