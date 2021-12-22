import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
print(new_dm)

# Setting default chart styles via Seaborn
sns.set_style("dark")
sns.set_palette("pastel")

# Creating a line chart to visualise the difference between the total and inflation adjusted gross incomes
dm_indexed = new_dm.set_index("release_date", drop=False)
dm_indexed.index = pd.to_datetime(dm_indexed.index)
fig, ax = plt.subplots()
ax.plot(dm_indexed.index, dm_indexed["total_gross"], label="Total gross (USD)")
ax.plot(dm_indexed.index, dm_indexed["inflation_adjusted_gross"], label="Inflation adjusted gross (USD)")
ax.set_title("Total and inflation adjusted gross income over time")
plt.legend()
plt.show()

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

# Creating a bar chart to compare the number of movies for each decade
dm_decades = ["30s", "40s", "50s", "60s", "70s", "80s", "90s", "00s", "10s"]
fig, ax = plt.subplots()
hbars = ax.barh(dm_decades, dm_decade_count)
ax.invert_yaxis()
ax.set_xlabel("Number of movies")
ax.set_ylabel("Decade")
ax.bar_label(hbars)
ax.set_xlim(right=275) # Adjust limit to fit labels
ax.set_title("Movies per decade")
plt.show()

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

# Creating a line chart to visualise the number of movies as well as total gross income for each decade
with sns.axes_style("darkgrid"):
    fig, ax1 = plt.subplots()
    ax1.set_title("Movies and income per decade")
    ax1.set_xlabel("Decade")
    ax1.plot(dm_decades, dm_decade_count, label="Number of movies", marker="o", linestyle="--", color="orange")
    ax1.set_ylabel("Number of movies")
    ax1.legend(loc="upper left")
    ax2 = ax1.twinx()
    ax2.plot(dm_decades, dm_decade_sum, label="Total gross income (USD)", marker="s", linewidth=0.5, color="blue")
    ax2.set_ylabel("Total gross income (USD)")
    ax2.legend(loc="lower right")
    plt.show()

# Grouping by genre to compare the total gross income (sum)
dm_grouped_sum = new_dm.groupby("genre")["total_gross"].sum()
print(dm_grouped_sum)

# Grouping by genre to compare the average gross income (mean)
dm_grouped_mean = new_dm.groupby("genre")["total_gross"].mean()
print(dm_grouped_mean)

# Creating a dictionary from an existing Series
dm_grouped_dict = dm_grouped_sum.to_dict()
print(dm_grouped_dict)

# Creating a pie chart to visualise the 5 genres that generated the highest gross income
dm_grouped_sum_top5 = dm_grouped_sum.nlargest(5)
fig, ax = plt.subplots()
ax.pie(dm_grouped_sum_top5, labels=dm_grouped_sum_top5.index)
ax.set_title("Top 5 genres (total gross income)")
plt.show()

# Creating a pie chart to visualise the 5 genres that generated the highest gross income in average
dm_grouped_mean_top5 = dm_grouped_mean.nlargest(5)
fig, ax = plt.subplots()
ax.pie(dm_grouped_mean_top5, labels=dm_grouped_mean_top5.index)
ax.set_title("Top 5 genres (average gross income)")
plt.show()

# Reusable function to calculate how many years ago a date is
def years_ago(date):
    year = datetime.fromisoformat(date).year
    return datetime.now().year - year

# Looping to present how many years ago the movies were released and how much gross income they generated
for label, row in dm.iterrows():
    print(row["movie_title"] + "  was released " + str(years_ago(row["release_date"])) + " years ago and generated " + str(row["total_gross"]) + " USD")
