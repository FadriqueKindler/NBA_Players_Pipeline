import requests
import pandas as pd
import os
import json
from bs4 import BeautifulSoup
import re


def getPlayers():
    players = pd.read_csv("./DATA/nba-players-stats/Players.csv")
    df_players = pd.DataFrame(players)
   
    df_players.drop(columns=["Unnamed: 0","birth_city","birth_state",],inplace=True)
    df_players = df_players.rename(columns={"height": "Height (m)","weight": "Weight (kg)",
                                            "collage": "College", "born" :"Born"})
    return df_players



def getPlayer_data():
    player_data = pd.read_csv("./DATA/nba-players-stats/player_data.csv")
    df_player_data = pd.DataFrame(player_data)
    
    df_player_data.drop(columns=["height","weight"],inplace=True)
    df_player_data = df_player_data.rename(columns={"name": "Player","year_start": "NBA_Rookie",
                                                    "year_end": "NBA_Retired","birth_date": "Birth Date",
                                                    "position": "Position", "college":"College"})
    return df_player_data


def getSeason_stats():
    season_stats = pd.read_csv("./DATA/nba-players-stats/Seasons_Stats.csv")
    df_season_stats = pd.DataFrame(season_stats)

    df_season_stats.drop(columns=["Unnamed: 0","blanl","blank2","Age","Year",],inplace=True)
    df_season_stats = df_season_stats[df_season_stats.Player.notnull()]
    df_season_stats = df_season_stats.dropna(thresh=50)
    return df_season_stats


def merging_dfs(df_players,df_player_data,df_season_stats):
    df_players_full = pd.merge(df_players,df_player_data ,how='outer', on='Player')
    complete_df = pd.merge(df_players_full,df_season_stats ,how='outer', on='Player')
    
    complete_df.drop_duplicates(subset ="Player", keep = "first", inplace = True)
    complete_df.drop(columns=["G","TS%","FTr","OWS","DWS","WS",
                              "FG","FGA","FG%","2P","2PA","2P%",
                              "eFG%","FT","FTA","AST","PF","PTS",
                              "College_x","College_y","FT%","GS",
                              "3PAr","TOV%","USG%","3P","3P%","3PA",
                              "TOV","BLK","STL","TRB","DRB","ORB","VORP",
                              "BPM","DBPM","OBPM","WS/48","BLK%","STL%","AST%",
                              "TRB%","DRB%","ORB%","MP","PER"],inplace=True)
    complete_df = complete_df.rename(columns={"Tm": "Team"})

    complete_df.to_csv('./DATA/nba-players-stats/DataSet_CompleteDf.csv')                      

    return complete_df



### WEBSCRAPING ###


URL = "https://ceoworld.biz/2019/03/05/these-are-50-highest-points-scorer-in-nba-history-1946-to-2019//"


def scan(URL): 
    results = requests.get(URL).text
    soup = BeautifulSoup(results, "html.parser")
    col_name = [element.text for element in soup.find_all("th")]
    player_info = [element.text for element in soup.find_all("td")]
    
    player_info_lst = []
    for ind in range(0, len(player_info), 11):
        player_info_lst.append(player_info[ind: (ind+11)])
    
    
    player_df = pd.DataFrame(player_info_lst)
    col_df = pd.DataFrame(col_name)
    return (player_df, col_df)


def wrangle_webscraping(player_df,col_df):

    col_df = col_df.transpose()
    col_df = col_df.rename(columns=col_df.iloc[0])
    player_df = player_df.rename(columns={0: "Rank", 1: "Player",2: "Points",3: "Seasons",
                                          4: "Games",5: "FGM",6: "FGA",7: "3PM",8: "3PA",
                                          9: "FTM",10: "FTA",})
 
    frames = [col_df, player_df]
    player_webScstats_df = pd.concat(frames) 
    player_webScstats_df = player_webScstats_df[player_webScstats_df.Rank != "Rank"]
    return player_webScstats_df



def wrangle_Best_50(player_webScstats_df):

    complete_df = pd.read_csv("./DATA/nba-players-stats/DataSet_CompleteDf.csv")

    top_player_lst = player_webScstats_df["Player"].tolist()
    top_player_df = complete_df[complete_df['Player'].isin(top_player_lst)]  ### CHECK CODE ###
    return top_player_df

def final_NBA50_df(player_webScstats_df, top_player_df):   ### DOES NOT LET ME MERGE ###
    master_player_df = pd.merge(top_player_df, player_webScstats_df ,how='left', on='Player')
    master_player_df = master_player_df[['Rank','Player','Points','FGM','FGA','3PM','3PA','FTM',
                                         'FTA','Games','Seasons','NBA_Rookie','NBA_Retired','Team',
                                         'Position','Birth Date','Height (m)','Weight (kg)',]]
    master_player_df.set_index('Player')
    
    master_player_df = master_player_df.replace(to_replace = "-", value = 0)
    master_player_df[["Rank", "Points","FGM","FGA","FTM","FTA","3PM","3PA","Games","Seasons"]] = master_player_df[["Rank", "Points","FGM","FGA","FTM","FTA","3PM","3PA","Games","Seasons"]].apply(pd.to_numeric)
    return master_player_df


def get_player_info(master_player_df):
    print(master_player_df["Player"])
    print("Enter Player Name:")
    x = input()
    pd.options.display.max_rows = 999
    print(master_player_df[master_player_df["Player"] == x]) 