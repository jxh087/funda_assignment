#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
# # Real Estate Reviews
# ##### By Jason Ji


# %% [markdown]
# ## Index

# %%
# pip install duckdb==0.9.2
# pip install nb_black
pip install functions_eda

# %%
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import functions_eda as eda

import duckdb

cursor = duckdb.connect()


# %%
# Load code beautyfier
# %load_ext nb_black

# %% [markdown]
# ### 0. Data Information

# %%
# Start a DuckDB session
csv_file_path = "Property Sales of Melbourne City.csv"

conn = duckdb.connect(database=":memory:", read_only=False)

# Load the CSV file into a DuckDB table
conn.execute(
    "CREATE TABLE property_sales AS SELECT * FROM read_csv_auto('{}')".format(
        csv_file_path
    )
)

# Run a SQL query on the loaded data

query = "SELECT * FROM property_sales LIMIT 10"

conn.sql(query).show()

result_df = conn.sql(query).df()


# %%
# Load the data
df = pd.read_csv("Property Sales of Melbourne City.csv")
df.head(5)


# %%
df.drop("Unnamed: 0", axis=1, inplace=True)
df.describe()

# %%
# Check for missing values
missing_values_percentage = (df.isnull().sum() / len(df)) * 100
missing_values_percentage = missing_values_percentage.sort_values(ascending=False)

print("\nMissing Values:")
for column, percentage in missing_values_percentage.items():
    print(f"{column}: {percentage:.2f}%")

# %%
# Check for duplicate entries
print("\nDuplicate Entries:")
print(df.duplicated().sum())

# %%
print("The original dataset has {0} observations".format(df.shape[0]))
print("The earlist selling date is {0}.".format(df.Date.min()))
print("The latest selling date is {0}.".format(df.Date.max()))

# %%
# Extracting year, month, and generating year-quarter
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Quarter"] = df["Date"].dt.quarter
df["Year_Quarter"] = df["Year"].astype(str) + "-Q" + df["Quarter"].astype(str)

df.to_excel("data_updated.xlsx")

# %% [markdown]
# ### 1.0 Market Share

# %%

# %%
# Group the df by year and month, and count the number of sales transactions in each group
monthly_sales_count = (
    df.groupby(["Year", "Month"]).size().reset_index(name="SalesCount")
)

# Create a line plot to visualize the monthly sales count
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")  # Set the style to white grid
sns.lineplot(
    data=monthly_sales_count,
    x="Year",
    y="SalesCount",
    hue="Month",
    palette="viridis",
    marker="o",
)
plt.title("Monthly Sales Count Over Time")
plt.xlabel("Year")
plt.ylabel("Sales Count")
plt.legend(
    title="Month",
    loc="upper right",
    labels=[
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ],
)
plt.xticks(rotation=45)
# Show the plot
plt.tight_layout()
plt.show()

# %%
