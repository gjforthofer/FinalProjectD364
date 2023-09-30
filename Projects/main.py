import pandas as pd


# Webscrape the data
# Store the data into pandas df
ptables = pd.read_html("https://www.basketball-reference.com/wnba/years/2023_advanced.html")
btables = pd.read_html("https://www.basketball-reference.com/wnba/years/2023_totals.html")
ttables = pd.read_html("https://www.basketball-reference.com/wnba/years/2023.html#all_totals-team-opponent")

playersAdv = ptables[0]
playersBasic = btables[0]
teamsAdvStats = ttables[7]
teamsOppStats = ttables[6]
teamsBasic = ttables[5]
playersAdv = playersAdv.dropna(axis=1, how='all')
playersBasic = playersBasic.dropna(axis=1, how='all')
teamsAdvStats = teamsAdvStats.dropna(axis=1, how='all')
teamsOppStats = teamsOppStats.dropna(axis=1, how='all')
teamsBasic = teamsOppStats.dropna(axis=1, how='all')


# Calculate VORP

#VORP columns
playersBasic['DRB'] = None
playersAdv['DRB%'] = None
playersAdv['gBPM'] = None
playersAdv['VORP'] = None 

#team mapping

team_mapping = {
    "ATL": "Atlanta Dream",
    "CHI": "Chicago Sky",
    "CON": "Connecticut Sun",
    "DAL": "Dallas Wings",
    "IND": "Indiana Fever",
    "LVA": "Las Vegas Aces",
    "LAS": "Los Angeles Sparks",
    "MIN": "Minnesota Lynx",
    "NYL": "New York Liberty",
    "PHO": "Phoenix Mercury",
    "SEA": "Seattle Storm",
    "WAS": "Washington Mystics",
}

playersAdv = playersAdv[playersAdv['Player'] != 'Player']
playersBasic = playersBasic[playersBasic['Player'] != 'Player']
playersAdv = playersAdv.reset_index(drop=True)
playersBasic = playersBasic.reset_index(drop=True)




playersAdv["Full Team Name"] = playersAdv["Team"].map(team_mapping)
playersBasic["Full Team Name"] = playersBasic["Team"].map(team_mapping)

teamsAdvStats.loc[:, ('Unnamed: 1_level_0', 'Team')] = teamsAdvStats[('Unnamed: 1_level_0', 'Team')].str.replace('*', '', regex=False)
teamsOppStats["Team name"] = teamsOppStats["Team"].str.replace('*', '', regex=False)
teamsBasic["Team name"] = teamsOppStats["Team"].str.replace('*', '', regex=False)

#for i in length(players):


# Stats acquired: MP, TeMP, GP, OR%, TR%, ST%, BLK%, Ast%, Usg%, TO%, TS%, TeTS%, 3Par, 

# Stats needed: Lg3Par, DRB%
sumLg3Par = 0
for i in range(len(teamsAdvStats)):
  sumLg3Par += teamsAdvStats.iloc[i].iloc[15]

Lg3Par = sumLg3Par/len(teamsAdvStats)

for i in range(len(playersBasic)):
  playersBasic = playersBasic[playersBasic["TRB"] != "TRB"]

  playersBasic["TRB"] = playersBasic["TRB"].astype(float)
  playersBasic["ORB"] = playersBasic["ORB"].astype(float)
  DRB = playersBasic.loc[i, "TRB"] - playersBasic.loc[i, "ORB"] 
  
  playersBasic.loc[i, "DRB"] = DRB
  MP = playersAdv.loc[i, "MP"]

  for j in range(len(teamsAdvStats)):
    if teamsOppStats.loc[j, "Team name"] == playersAdv.loc[i, "Full Team Name"] and teamsBasic.loc[j, "Team name"] == playersAdv.loc[i, "Full Team Name"]:
      TeMP = teamsBasic.loc[j,"MP"]
      TmDRB = teamsBasic.loc[j, "DRB"]
      OppDRB = teamsOppStats.loc[j, "DRB"]

  DRB = float(DRB)
  TeMP = float(TeMP)
  MP = float(MP)
  TmDRB = float(TmDRB)
  OppDRB = float(OppDRB)

  DRBp = 100*((DRB*(TeMP/5))/(MP * (TmDRB+OppDRB)))
  playersAdv[i, "DRB%"] = DRBp





print(playersAdv.iloc[0])


#for i in range(len(players)):

# VORP = [BPM - (-2)] * (5*MP/TeMP)*(TeGP/LgGP)

  # BPM = gBPM + TeAdC

    # gBPM = gBPM1 + gBPM2 + gBPM3 + gBPM4 + gBPM5 + gBPM6 + gBPM7 + gBPM8 + gBPM9

      # gBPM1 = 0.123391 * (MP/(GP + 2))
  #gBPM1 = 0.123391 * (players.iloc[i].iloc[6]/((players.iloc[i].iloc[5])+2))
      # gBPM2 = 0.119597 * OR%
  #gBPM2 = 0.119597 * (players.iloc[i].iloc[12])
      # gBPM3 = -0.151287 * DR%
  #gBPM3 = -0.151287 * 
      # gBPM4 = 1.255644 * ST%

      # gBPM5 = 0.531838 * BLK%

      # gBPM6 = -0.305868 * Ast%

      # gBPM7 = 0.921292 * Usg% * TO%

      # gBPM8 = 0.711217 * Usg% * (1-TO%) * [2 * (TS% - TmTS%) + 0.017022 * Ast% + 0.297639 (3P% - Lg3P%) - 0.213485]

      #gBPM9 = 0.72593 * sqrt(Ast% * TR%)
  #gBPM = gBPM1 + gBPM2 + gBPM3 + gBPM4 + gBPM5 + gBPM6 + gBPM7 + gBPM8 + gBPM9

