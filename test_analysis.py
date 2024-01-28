#!/usr/bin/env python
# coding: utf-8
# %%
#pip install duckdb==0.9.2


# %%
import duckdb
cursor = duckdb.connect()


# %%
#Start a DuckDB session
csv_file_path = 'Property Sales of Melbourne City.csv'

conn = duckdb.connect(database=':memory:', read_only=False)

# Load the CSV file into a DuckDB table
conn.execute("CREATE TABLE property_sales AS SELECT * FROM read_csv_auto('{}')".format(csv_file_path))

# Run a SQL query on the loaded data

query = "SELECT * FROM property_sales LIMIT 10"

conn.sql(query).show()

result_df = conn.sql(query).df()


# %%




