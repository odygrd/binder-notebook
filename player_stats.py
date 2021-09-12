import io
import datetime as dt
import pandas as pd
from tabulate import tabulate
from datetime import datetime
import os
import seaborn as sns

# Returns the file with the latest date
def get_latest_player_stats_file():
    dates = []
    for file in os.listdir("input/player_stats"):
        #     e.g. 2021-09-01.csv
        filename = file.split("_")[-1]
        date = filename.split(".")[0]
        dates.append(date)

    # Sort the list in ascending order of dates 
    dates.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d'))
    
    return "input/player_stats/player_stats_{}.csv".format(dates[-1])

df = pd.read_csv(get_latest_player_stats_file())

sum_column = df["Attack"] + df["Defense"]
df["Total (Att+Def)"] = sum_column
column_names = ["Score", "Name", "Era", "Attack", "Defense", "Total (Att+Def)", "Guild Goods"]
df = df.reindex(columns=column_names)
df.set_index('Era',inplace=True)

# Calculate Averages
df_mean = df.groupby('Era').mean()
df_mean = df_mean.drop(columns='Attack')
df_mean = df_mean.drop(columns='Defense')
df_mean = df_mean.drop(columns='Score')
df_mean = df_mean.rename(columns={"Total (Att+Def)": "Era average Att+Def", "Guild Goods": "Era average Guild Goods"})

# Join into a single df
df_final = df.join(df_mean)
column_names = ["Score", "Name", "Attack", "Defense", "Total (Att+Def)", "Era average Att+Def", "Guild Goods", "Era average Guild Goods"]
df_final = df_final.reindex(columns=column_names)
df_final.set_index('Score', inplace=True)
df_final.sort_index(ascending=False,inplace=True)
df_final.reset_index(drop=True, inplace=True)
print(tabulate(df_final, headers='keys', tablefmt='fancy_grid'))

styled_df = df_final.style.background_gradient(cmap=sns.light_palette("green", as_cmap=True), subset=pd.IndexSlice[df_final['Guild Goods']>=2357, 'Guild Goods']).background_gradient(cmap=sns.light_palette("red", as_cmap=True, reverse=True), subset=pd.IndexSlice[df_final['Guild Goods']<2357, 'Guild Goods']).background_gradient(cmap=sns.light_palette("purple", as_cmap=True), subset=['Total (Att+Def)']).format(precision = 0).set_table_styles([{"selector": "", "props": [("border", "1px solid grey")]},{"selector": "tbody td", "props": [("border", "1px solid grey")]},{"selector": "th", "props": [("border", "1px solid grey")]}])

with open('df_html.html', 'w') as html:
    html.write(styled_df.render())


