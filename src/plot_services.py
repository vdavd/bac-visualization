import math
import os
from datetime import datetime, timedelta
from flask import session
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg') # matplotlib crashes flask wihout this

# takes a list with user and drinks information generated by get_user_drinks function
def calculate_bac(user_drinks):
    user_sex = user_drinks[0].sex
    user_weight = user_drinks[0].user_weight
    user_height = user_drinks[0].user_height
    user_age = user_drinks[0].user_age
    username = user_drinks[0].username
    time_now = datetime.now()
    start_time = time_now - timedelta(hours=24)

    elimination_rate = 0.18 # average rate at which alcohol is eliminated from the blood
    k = 4.4 # absorption rate constant (k) is 6.5 for full stomach and 2.3 for empty, 4.4 is average
    if user_sex == "male":
        q_value = (0.3362*user_weight) + (10.74*(user_height/100)) - (0.09516*user_age) + 2.447
    elif user_sex == "female":
        q_value = (0.2466*user_weight) + (10.69*(user_height/100)) - 2.097

    bac_df = pd.DataFrame([[username, 0, start_time]], columns=["username", "bac", "time"])

    bac = 0
    alc_eliminated = 0
    for i in range(1, 360):
        time = start_time + timedelta(minutes=i*6)
        if bac > 0:
            alc_eliminated += min(elimination_rate*0.1, bac)
        bac = 0
        if user_drinks[0].drink_id:
            for drink in user_drinks:
                if drink.drink_time < start_time or drink.drink_time > time:
                    continue
                else:
                    time_difference = time - drink.drink_time
                    tn = time_difference.total_seconds()/3600
                    bac += (0.8*(drink.alcohol_content*(1-math.exp(-k*tn))))/q_value
            bac -= alc_eliminated
            bac = max(0, bac)
        bac_df.loc[i] = [username, bac, time]

    return bac_df, time_now


def plot_bac(bac_df, time_now):
    id = session["id"]
    time_now = datetime(time_now.year, time_now.month, time_now.day, time_now.hour)
    xticks = [time_now + timedelta(hours=i) for i in range(-12, 13)]
    start_date = (time_now-timedelta(hours=12)).strftime("%Y/%m/%d")
    end_date = (time_now+timedelta(hours=12)).strftime("%Y/%m/%d")
    try:
        os.remove(f"static/bacplot_user_{id}.png")
    except:
        pass
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 4.6))
    bac_plot = sns.lineplot(x="time", y="bac", hue="username", data=bac_df)
    bac_plot.set_xlim(xticks[0], xticks[-1])
    bac_plot.set_xticks(xticks)
    bac_plot.set_xticklabels([x.hour for x in xticks])
    bac_plot.set(ylabel="Blood alcohol concentration (‰)", \
                 xlabel=f"Time (hours), {start_date} - {end_date}")
    sns.move_legend(bac_plot, "lower center", ncol=5, \
                    bbox_to_anchor=(0.5, 1), title=None, frameon=False)
    plt.savefig(f"static/bacplot_user_{id}.png", bbox_inches="tight", dpi=150)
    plt.close("all")

def plot_room_bac(bac_df, time_now, room_id):
    time_now = datetime(time_now.year, time_now.month, time_now.day, time_now.hour)
    xticks = [time_now + timedelta(hours=i) for i in range(-12, 13)]
    try:
        os.remove(f"static/bacplot_room_{room_id}.png")
    except:
        pass
    start_date = (time_now-timedelta(hours=12)).strftime("%Y/%m/%d")
    end_date = (time_now+timedelta(hours=12)).strftime("%Y/%m/%d")
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 4.6))
    bac_plot = sns.lineplot(x="time", y="bac", hue="username", data=bac_df)
    bac_plot.set_xlim(xticks[0], xticks[-1])
    bac_plot.set_xticks(xticks)
    bac_plot.set_xticklabels([x.hour for x in xticks])
    bac_plot.set(ylabel="Blood alcohol concentration (‰)", \
                 xlabel=f"Time (hours), {start_date} - {end_date}")
    sns.move_legend(bac_plot, "lower center", ncol=5, \
                    bbox_to_anchor=(0.5, 1), title=None, frameon=False)
    plt.savefig(f"static/bacplot_room_{room_id}.png", bbox_inches="tight", dpi=150)
    plt.close("all")

def concatenate_dataframes(dataframes):
    return pd.concat(dataframes, ignore_index=True)
