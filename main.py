import pandas as pd
import numpy as np
from datetime import datetime

# Reading Disney Movies CSV
dm = pd.read_csv("disney_movies.csv")
print(dm.head())
print(dm.shape)

# Detecting missing data
print(dm.isna().any())

# Replacing missing values
new_dm = dm.fillna("Unknown")

# Checking if it worked
print(new_dm.isna().any())

# Sorting by total gross income
dm_income = new_dm.sort_values("total_gross", ascending=False)
print(dm_income.head())

# Sorting by inflation adjusted gross
dm_income_adj = new_dm.sort_values("inflation_adjusted_gross", ascending=False)
print(dm_income_adj.head())

# Adding a new column that shows the difference between the total and inflation adjusted gross incomes
new_dm["adjusted_gross_difference"] = new_dm["inflation_adjusted_gross"] - new_dm["total_gross"]
print(dm)

# Setting an index and sorting based on that index, before slicing
dm_srt = new_dm.set_index("release_date", drop=False).sort_index()

# Slicing by date
# Getting data for movies with a release date between 1937-01-01 and 2000-12-31, and between 2001-01-01 and 2016-12-31
dm_older = dm_srt.loc["1937":"2001"]
dm_recent = dm_srt.loc["2001":"2017"]
print(dm_older)
print(dm_recent)

# Counting the number of movies for each date range
print(str(dm_older["movie_title"].count()) + " movies released between 1937 and 2000, and " + str(dm_recent["movie_title"].count()) + " movies released between 2001 and 2016.")

# Merging data frames
frames = [dm_older, dm_recent]
result = pd.concat(frames)
print(dm_srt)
print(result)

# Counting the number of movies for each decade
dm_decade_count = np.array([
    len(dm_srt["1937":"1940"]),
    len(dm_srt["1940":"1950"]),
    len(dm_srt["1950":"1960"]),
    len(dm_srt["1960":"1970"]),
    len(dm_srt["1970":"1980"]),
    len(dm_srt["1980":"1990"]),
    len(dm_srt["1990":"2000"]),
    len(dm_srt["2000":"2010"]),
    len(dm_srt["2010":"2016"])
])
print(dm_decade_count)

# Calculating the total gross income for each decade
dm_decade_sum = np.array([
    dm_srt["1937":"1940"]["total_gross"].sum(),
    dm_srt["1940":"1950"]["total_gross"].sum(),
    dm_srt["1950":"1960"]["total_gross"].sum(),
    dm_srt["1960":"1970"]["total_gross"].sum(),
    dm_srt["1970":"1980"]["total_gross"].sum(),
    dm_srt["1980":"1990"]["total_gross"].sum(),
    dm_srt["1990":"2000"]["total_gross"].sum(),
    dm_srt["2000":"2010"]["total_gross"].sum(),
    dm_srt["2010":"2016"]["total_gross"].sum()
])
print(dm_decade_sum)

# Grouping by genre to compare the total gross income (sum)
dm_grouped_sum = new_dm.groupby("genre")["total_gross"].sum()
print(dm_grouped_sum)

# Grouping by genre to compare the average gross income (mean)
dm_grouped_mean = new_dm.groupby("genre")["total_gross"].mean()
print(dm_grouped_mean)

# Creating a dictionary from an existing Series
dm_grouped_dict = dm_grouped_sum.to_dict()
print(dm_grouped_dict)

# Reusable function to calculate how many years ago a date is
def years_ago(date):
    year = datetime.fromisoformat(date).year
    return datetime.now().year - year

# Looping to present how many years ago the movies were released and how much gross income they generated
for label, row in dm.iterrows():
    print(row["movie_title"] + "  was released " + str(years_ago(row["release_date"])) + " years ago and generated " + str(row["total_gross"]) + " USD")
