import requests
import pandas as pd
import os
import json
from bs4 import BeautifulSoup
import re
#from TRIALS import getPlayers, getPlayer_data, getSeason_stats, merging_dfs
#from WebScraping import scan, wrangle_webscraping, wrangle_Best_50, final_NBA50_df, get_player_info
from Functions import getPlayers, getPlayer_data, getSeason_stats, merging_dfs, scan, wrangle_webscraping, wrangle_Best_50, final_NBA50_df, get_player_info

URL = "https://ceoworld.biz/2019/03/05/these-are-50-highest-points-scorer-in-nba-history-1946-to-2019//"

def main():
 
    df_players = getPlayers()
    df_player_data = getPlayer_data()
    df_season_stats = getSeason_stats()

    complete_df_merge = merging_dfs(df_players,df_player_data,df_season_stats)

    player_df, col_df = scan(URL)

    player_finalstats_df = wrangle_webscraping(player_df, col_df) 
    filtered_50_best = wrangle_Best_50(player_finalstats_df)

    final_NBA50 = final_NBA50_df(player_finalstats_df, filtered_50_best)
    NBA_player_stats = get_player_info(final_NBA50)
    return NBA_player_stats

    

if __name__ == '__main__':
    main()