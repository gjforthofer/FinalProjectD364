import pandas as pd


# Webscrape the data
# Store the data into pandas df
dfplayers = pd.read_html("https://www.basketball-reference.com/wnba/years/2023_advanced.html")
dfteams = pd.read_html("https://www.basketball-reference.com/wnba/years/2023.html#all_totals-team-opponent")


# Calculate Advanced Stats

