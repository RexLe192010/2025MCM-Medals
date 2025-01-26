import pandas as pd
import csv
import os

def compute_count(data):
    years = data["Year"].unique()
    counts = {}
    for year in years:
        year_data = data[data["Year"] == year]
        for sport in year_data["Sport"].unique():
            if sport not in counts:
                counts[sport] = 0
            counts[sport] += 1
    return counts


def construct_df(athletes_data, hosts_data, counts):
    new_data = []
    for sport in counts:
        # filter sports with more than 5 occurrences
        if counts[sport] > 5:
            filtered_data = athletes_data[athletes_data["Sport"] == sport]
            print(filtered_data.head())
            new_data.append(filtered_data)
    
    new_df = pd.concat(new_data, ignore_index=True)
    print(new_df.head())

    #  count the number of unique sports
    sports = new_df["Sport"].unique()
    # print(sports)
    # print(len(sports))

    results = []

    # group by Sport, Year, and Team to calculate required statistics
    for sport in sports:
        sport_data = new_df[new_df["Sport"] == sport]
        # print(sport_data.head())
        years = sport_data["Year"].unique()
        # print(len(years))
        for year in years:
            year_data = sport_data[sport_data["Year"] == year]
            # print(year_data.head())
            teams = year_data["Team"].unique()
            # print(sport)
            # print(year)
            # print(teams)
            countries = {}
            for team in teams:
                if '-' in team: # team with hyphen means it's one of the many teams of a country
                    country = team.split('-')[0]
                else:
                    country = team
                
                # if the country is not in the dictionary, add it
                if country not in countries:
                    countries[country] = [0, 0, 0, 0, 0] # gold, silver, bronze, total medals, participants

                # extract the data for this team in this year
                team_data = year_data[year_data["Team"] == team]
                # print(team_data.head())

                # compute the number of gold medal for this team in this year
                gold_medals = team_data[team_data["Medal"] == "Gold"]
                unique_gold_medals = gold_medals["Event"].nunique()
                countries[country][0] += unique_gold_medals

                # compute the number of silver medal for this team in this year
                silver_medals = team_data[team_data["Medal"] == "Silver"]
                unique_silver_medals = silver_medals["Event"].nunique()
                countries[country][1] += unique_silver_medals

                # compute the number of bronze medal for this team in this year
                bronze_medals = team_data[team_data["Medal"] == "Bronze"]
                unique_bronze_medals = bronze_medals["Event"].nunique()
                countries[country][2] += unique_bronze_medals

                # compute the total number of medals for this team in this year
                unique_total_medals = unique_gold_medals + unique_silver_medals + unique_bronze_medals
                countries[country][3] += unique_total_medals

                # compute the number of participants for this team in this year
                participants = team_data["Name"].nunique()
                countries[country][4] += participants

                # results.append(
                #     {
                #         "Sport": sport,
                #         "Year": year,
                #         "Team": team,
                #         "gold_medals": unique_gold_medals,
                #         "silver_medals": unique_silver_medals,
                #         "bronze_medals": unique_bronze_medals,
                #         "total_medals": unique_total_medals,
                #         "participants": participants
                #     }
                # )
            for country in countries:
                results.append(
                    {
                        "Sport": sport,
                        "Year": year,
                        "Team": country,
                        "gold_medals": countries[country][0],
                        "silver_medals": countries[country][1],
                        "bronze_medals": countries[country][2],
                        "total_medals": countries[country][3],
                        "participants": countries[country][4]
                    }
                )

    # Calculate total medals and participants for each sport and year
    sport_year_grouped = new_df.groupby(["Sport", "Year"]).agg(
        sport_total_medals=("Event", "nunique"),
        sport_total_participants=("Name", "count")
    ).reset_index()

    sport_year_grouped["sport_total_medals"] *= 3 # Each event has 3 medals

    # Merge the grouped dataframes
    final_df = pd.merge(pd.DataFrame(results), sport_year_grouped, on=["Sport", "Year"])

    # merge with hosts data
    final_df = pd.merge(final_df, hosts_data[["Year", "Host"]], on="Year", how="left")

    final_df["isHost"] = (final_df["Team"] == final_df["Host"]).astype(int)

    final_df = final_df.drop(columns=["Host"], axis=1)

    return final_df

if __name__ == "__main__":
    # Load the data
    athletes_data = pd.read_csv("processed/summerOly_athletes_cleaned.csv")
    hosts_data = pd.read_csv("processed/summerOly_hosts_cleaned.csv")
    # Display the first 5 rows
    # print(athletes_data.head())

    # US_2004_Athletics = athletes_data[(athletes_data["Year"] == 2004) & (athletes_data["Team"] == "United States") & (athletes_data["Sport"] == "Athletics")]
    # US_2004_Athletics.to_csv("US_2004.csv", index=False)

    counts = compute_count(athletes_data)

    new_df = construct_df(athletes_data, hosts_data, counts)
    print(new_df.head())
    new_df.to_csv("processed/gt5_sports.csv", index=False)
    # print(new_df.head())