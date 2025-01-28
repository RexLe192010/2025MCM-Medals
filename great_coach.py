import pandas as pd
import csv
import plotly.express as px
import matplotlib.pyplot as plt

def generate_line_plot(data, country, sport):
    # filter out the rows for China and Volleyball
    china_volleyball = data[(data["Team"] == country) & (data["Sport"] == sport)]
    # sort the data by year
    china_volleyball = china_volleyball.sort_values(by="Year")

    # generate a line plot for the number of gold/total medals in the sport for the country
    fig = px.line(china_volleyball, x="Year", y=["gold_medals", "total_medals"], 
                  title=f"Number of Gold and Total Medals in {sport} for {country}")

    # update layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Medals",
        legend_title="Medal Type"
    )

    # display the plot
    fig.show()




if __name__ == "__main__":
    # Load the data
    lt5_sports = pd.read_csv("processed/lt5_sports.csv")
    gt5_sports = pd.read_csv("processed/gt5_sports.csv")

    # generate line plot for China and Volleyball
    generate_line_plot(gt5_sports, "China", "Volleyball")

    # generate line plot for USA and Volleyball
    generate_line_plot(gt5_sports, "United States", "Volleyball")

    # generate line plot for Romania and Gymnastics
    generate_line_plot(gt5_sports, "Romania", "Gymnastics")

    # generate line plot for USA and Gymnastics
    generate_line_plot(gt5_sports, "United States", "Gymnastics")

    # generate line plot for 