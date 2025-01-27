import pandas as pd
import plotly.express as px


# 1. 一个treemap diagram，2024年sport奖牌分布
# 2. 2024奖牌前15名的国家，他们总奖牌数的折线图和金牌数折线图
# 3. 流程图（在做classification时的标准，流程等）

def treemap_diagram(data):
    # filter out the data for 2024
    data_2024 = data[data["Year"] == 2024]

    # group the data by Sport
    medal_2024 = (
        data_2024.groupby("Sport")["Event"]
        .nunique()
        .reset_index()
        .rename(columns={"Event": "Total Medals"})
    )

    medal_2024["Total Medals"] *= 3  # Each event has 3 medals

    # use plotly express to create the treemap diagram
    fig = px.treemap(
        medal_2024,
        path=["Sport"],
        values="Total Medals",
        color="Total Medals",
        title="2024 Olympic Games Medal Distribution by Sport",
    )

    # display values on the treemap diagram
    fig.update_traces(textinfo="label+value")

    fig.show()


def compute_top15_2024(data): # here, the data should be the medal_counts
    # filter out the data for 2024
    data_2024 = data[data["Year"] == 2024]
    countries = set()

    for country in data_2024["NOC"].unique():
        country_data = data_2024[data_2024["NOC"] == country]
        rank = country_data["Rank"].iloc[0]
        if rank <= 15:
            countries.add(country)
    
    return countries


def top15_medals_lineplot(data, top15_countries): # here, the data should be the medal_counts
    # filter out the data for top 15 countries in 2024
    data_top15 = data[data["NOC"].isin(top15_countries)]

    fig = px.line(
        data_top15,
        x="Year",
        y="Total",
        color="NOC",
        title="Total Medals of Top 15 Countries in 2024 Olympic Games",
    )
    
    fig.show()

    fig = px.line(
        data_top15,
        x="Year",
        y="Gold",
        color="NOC",
        title="Gold Medals of Top 15 Countries in 2024 Olympic Games",
    )

    fig.show()


def turnover_medals_lineplot(data):
    # as what I did in stability_classification.py, compute the turnover of all sports
    turnovers = []
    # filter data for the most recent 6 olympic games
    filtered_data = data[data["Year"] >= 2004]

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
    

    pass


if __name__ == "__main__":
    # Load the data
    athletes_data = pd.read_csv("processed/summerOly_athletes_cleaned.csv")
    medal_counts = pd.read_csv("processed/summerOly_medal_counts_cleaned.csv")

    # treemap diagram, 2024 Olympic Games Medal Distribution by Sport
    treemap_diagram(athletes_data)

    # top 15 countries in 2024
    top15_countries = compute_top15_2024(medal_counts)

    # line plot, total medals and gold medals of top 15 countries in 2024
    top15_medals_lineplot(medal_counts, top15_countries)