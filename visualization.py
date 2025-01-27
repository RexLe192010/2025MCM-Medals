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