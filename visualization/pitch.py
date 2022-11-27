import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from mplsoccer.pitch import VerticalPitch
import seaborn as sns
import matplotlib.patheffects as pe
from scipy.ndimage import gaussian_filter

#Root directory of the project
ROOT_DIR = os.path.abspath("../")

#to find local version of the library
sys.path.append(ROOT_DIR)



def makepitch():
    #draw the pitch
    fig,ax = plt.subplots(figsize=(16,11))
    fig.set_facecolor('#22312b')
    ax.patch.set_facecolor('#22312b')
    pitch = Pitch(pitch_type='statsbomb', half=False, pitch_length=120, pitch_width=80,
             pitch_color='#22312b', line_color='#c7d5cc')
    pitch.draw(ax=ax)
   
    
def passmap(data, player, time_start=0, time_ends=90):
    makepitch()
    df_player = data[(data["PlayerName"] == player) & (data["Mins"] >= time_start) & (data["Mins"] <=time_ends)]
    df_player.index = np.arange(0, len(df_player))
    #draw the player movements
    for x in range(len(df_player)):
        plt.plot([int(df_player["X"][x]), int(df_player["X2"][x])], [int(df_player["Y"][x]), int(df_player["Y2"][x])], color='green')
        plt.scatter(int(df_player["X"][x]), int(df_player["Y"][x]), color="green")

    if (time_start == 0) and (time_ends == 90):
        plt.title(label="The pass and dribble of "+player+" for entire match", color="white", fontsize=20)
    elif (time_start == 0) and (time_ends == 45):
        plt.title(label="The pass and dribble of "+player+" for first half", color="white", fontsize=20)
    elif (time_start == 45) and (time_ends == 90):
        plt.title(label="The pass and dribble of "+player+" for second half", color="white", fontsize=20)
    else:
        time = time_ends - time_start
        plt.title(label="The pass and dribble of "+player+" for " + str(time)+" minutes", color="white", fontsize=20)

def passweb(passdata):
    #grouping the total pass by the players
    avg_location = passdata.groupby(["Passer", "PasserName"], as_index=False).agg({"X":["mean"], "Y":["mean", "count"]})
    avg_location.columns = ["PlayerNum", "PlayerName", "Xmean", "Ymean", "TotalPass"]
    avg_location.set_index("PlayerNum", inplace=True)
    
    pass_between = passdata.groupby(["Passer","PasserName","Recipient","RecipientName"]).row_num.count().reset_index()
    pass_between.rename({"row_num":"Pass_Count"}, axis="columns", inplace=True)
    pass_between = pass_between.merge(avg_location, left_on="Passer", right_index=True)
    pass_between = pass_between.merge(avg_location, left_on="Recipient", right_index=True, suffixes=["","_end"])
    field = Pitch(pitch_type='statsbomb', half=False, pitch_length=120, pitch_width=80,
             pitch_color='#22312b', line_color='#c7d5cc')
    fig,ax = field.draw(figsize=(16,11))
    nodes = field.scatter(avg_location.Xmean, avg_location.Ymean, s=300*avg_location.TotalPass, color="white", edgecolor="#2db9ff",
                          linewidth=4, alpha=1, zorder=1, ax=ax)
    arrows = field.lines(pass_between.Xmean, pass_between.Ymean, pass_between.Xmean_end, pass_between.Ymean_end, ax=ax, 
                         lw=pass_between.Pass_Count, color="white", zorder = 4, alpha=.5)
    for x, row in avg_location.iterrows():
        field.annotate(row.PlayerName, xy=(row.Xmean, row.Ymean), color="black", va='center', ha='center', weight = "bold", 
                       size=20, ax=ax, wrap=True, zorder = 4,
                       path_effects=[pe.withStroke(linewidth=5, foreground="white")]
                       )
    plt.title(label="Pass Web Between England Players", color="black", fontsize=20)

def playerheatmap(data, player, time_start=0, time_ends=90):
    pitch = Pitch(pitch_type='statsbomb', line_zorder=2,
                  pitch_color='#22312b', line_color='#c7d5cc')
    fig,ax = pitch.draw(figsize=(16,11))
    fig.set_facecolor("#22312b")
    time = time_ends - time_start
    df_player = data[(data["PlayerName"] == player) & (data["Mins"] >= time_start) & (data["Mins"] <=time_ends)]
    df_player.index = np.arange(0, len(df_player))
    bin_stat=pitch.bin_statistic(df_player.X, df_player.Y,
                                 statistic="count", bins=(25,25))
    bin_stat["statistic"] = gaussian_filter(bin_stat["statistic"],1)
    pitch_heatmap = pitch.heatmap(bin_stat, ax=ax, cmap="hot")
    #kde = sns.kdeplot(x=df_player["X"], y=df_player["Y"], fill=True, 
                      #thresh=(len(data)-len(df_player))/len(data), n_levels=len(data),
                      #alpha=.5, levels=len(df_player), cmap="Spectral_r",
                      #linewidth=0)

    
    if (time_start == 0) and (time_ends == 90):
        plt.title(label="The pass and dribble of "+player+" for entire match", color="white", fontsize=20)
    elif (time_start == 0) and (time_ends == 45):
        plt.title(label="The pass and dribble of "+player+" for first half", color="white", fontsize=20)
    elif (time_start == 45) and (time_ends == 90):
        plt.title(label="The pass and dribble of "+player+" for second half", color="white", fontsize=20)
    else:
        time = time_ends - time_start
        plt.title(label="The pass and dribble of "+player+" for " + str(time)+" minutes", color="white", fontsize=20)
    
