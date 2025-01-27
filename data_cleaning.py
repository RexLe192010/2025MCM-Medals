import pandas as pd
import csv
import os


def change_countryname(data):
    # 1. 德国=东德+西德
    # 2. 俄罗斯直接继承所有USSR的奖牌，其它分裂的国家按新参与者计算
    # 3. 塞尔维亚直接继承所有Yugoslavia的奖牌，其它按新参与者算
    # 4. Czech Republic直接继承所有Czechoslovakia的奖牌，Slovakia按新参与者算

    # create a copy of the data
    data_copy = data.copy()

    # 1. replace East Germany and West Germany with Germany
    data_copy.replace(r"^East Germany.*", "Germany", inplace=True, regex=True)
    data_copy.replace(r"^West Germany.*", "Germany", inplace=True, regex=True)

    # 2. replace USSR with Russia
    data_copy.replace(r"^Soviet.*", "Russia", inplace=True, regex=True)

    # 3. replace Yugoslavia with Serbia
    data_copy.replace(r"^Yugoslavia.*", "Serbia", inplace=True, regex=True)

    # 4. replace Czechoslovakia with Czech Republic
    data_copy.replace(r"^Czechoslovakia.*", "Czech Republic", inplace=True, regex=True)

    # write the data to a new file
    data_copy.to_csv("summerOly_athletes_country.csv", index=False)

    return data_copy


def change_sports(data):
    # 1. Canoeing在2020和2024分为了Canoe Slalom 和Canoe Sprint, 直接搜索substring canoe 合并
    # 2. Cycling在2020和2024拆成了很多项目，直接substring cycling合并
    # 3. Equestrian用这个substring，和equestrianism合并起来
    # 4. 所有gymnastics 用 gymnastics这个substring合并，再把trampolining 手动加进来
    # 5. synchronized swimming和artistic swimming合并，这个可能无法substring搜索

    # create a copy of the data
    data_copy = data.copy()

    sport_column = data_copy["Sport"]

    # 1. replace Canoe Slalom and Canoe Sprint with Canoeing
    sport_column.replace(r".*Canoe.*", "Canoeing", inplace=True, regex=True)

    # 2. replace all cycling events with Cycling
    sport_column.replace(r".*Cycling.*", "Cycling", inplace=True, regex=True)

    # 3. replace Equestrian with Equestrianism
    sport_column.replace(r"^Equestrian.*", "Equestrianism", inplace=True, regex=True)

    # 4. replace all gymnastics events with Gymnastics
    sport_column.replace(r".*Gymnastics.*", "Gymnastics", inplace=True, regex=True)
    sport_column.replace(r".*Trampolining.*", "Gymnastics", inplace=True, regex=True)

    # 5. replace Synchronized Swimming and Artistic Swimming with Swimming
    sport_column.replace(r".*Swimming.*", "Swimming", inplace=True, regex=True)

    data_copy["Sport"] = sport_column

    return data_copy


if __name__ == "__main__":
    # Load the data
    athletes_data = pd.read_csv("raw/summerOly_athletes.csv")
    hosts_data = pd.read_csv("raw/summerOly_hosts.csv")
    medal_counts = pd.read_csv("raw/summerOly_medal_counts.csv")
    # Display the first 5 rows
    # print(athletes_data.head())

    data_country = change_countryname(athletes_data)
    data_sports = change_sports(data_country)
    data_sports.to_csv("processed/summerOly_athletes_cleaned.csv", index=False)

    # clean the medal counts data
    new_medal_counts = change_countryname(medal_counts)
    new_medal_counts.to_csv("processed/summerOly_medal_counts_cleaned.csv", index=False)