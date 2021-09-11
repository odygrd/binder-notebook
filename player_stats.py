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
df_final.set_index('Score', inplace=True)
df_final.sort_index(ascending=False,inplace=True)

print(tabulate(df_final, headers='keys', tablefmt='fancy_grid'))

# cm = sns.light_palette("green", as_cmap=True)
# styled_df = df_final.style.background_gradient(cmap=cm, subset=['Guild Goods'])

# with open('df_html.html', 'w') as html:
#     html.write(styled_df.render())

