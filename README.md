# NBA_Players_Pipeline
Shows you the full stats for the 50 high scorers in NBA history

## Files

-> Functions.py:

-- Contains all the functions in the pipeline. It is separated into three distinct parts:

- Imports all 3 csv´s with player data and stats and merges them into 1 full dataframe. Then the dataframe is wrangled in order to keep only the stats we want.
- Webscraping of url ("https://ceoworld.biz/2019/03/05/these-are-50-highest-points-scorer-in-nba-history-1946-to-2019//"). We acquire the table contents and we create a dataframe with the rank of all 50 players. 
- Merging of both dataframes and further wrangling to keep just the desired features.

-> Main.py:

-- The fully functional pipeline. It returns the list of all 50 players and asks the user to input the name of the desired player. It then returns all stats for the selected player.

