import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from mplsoccer.pitch import VerticalPitch
import seaborn as sns

#Root directory of the project
ROOT_DIR = os.path.abspath("../")

#to find local version of the library
sys.path.append(ROOT_DIR)

def makepitch():
    #draw the pitch
    fig,ax = plt.subplots(figsize=(12, 8))
    fig.set_facecolor('#22312b')
    ax.patch.set_facecolor('#22312b')
    pitch = Pitch(pitch_type='statsbomb', half=False, pitch_length=120, pitch_width=80,
             pitch_color='#22312b', line_color='#c7d5cc')
    pitch.draw(ax=ax)
   
    
def passmap(data, player, time_start=0, time_ends=90):
    makepitch()
    df_player = data[(data["Player"] == player) & (data["Mins"] >= time_start) & (data["Mins"] <=time_ends)]
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


def playerheatmap(data, player, time_start=0, time_ends=90):
    makepitch()
    time = time_ends - time_start
    df_player = data[(data["Player"] == player) & (data["Mins"] >= time_start) & (data["Mins"] <=time_ends)]
    df_player.index = np.arange(0, len(df_player))
    
    kde = sns.kdeplot(x=df_player["X"], y=df_player["Y"], fill=True, 
                      thresh=(len(data)-len(df_player))/len(data), n_levels=len(data),
                      alpha=.5, levels=len(df_player), cmap="Spectral_r",
                      linewidth=0)

    
    if (time_start == 0) and (time_ends == 90):
        plt.title(label="The pass and dribble of "+player+" for entire match", color="white", fontsize=20)
    elif (time_start == 0) and (time_ends == 45):
        plt.title(label="The pass and dribble of "+player+" for first half", color="white", fontsize=20)
    elif (time_start == 45) and (time_ends == 90):
        plt.title(label="The pass and dribble of "+player+" for second half", color="white", fontsize=20)
    else:
        time = time_ends - time_start
        plt.title(label="The pass and dribble of "+player+" for " + str(time)+" minutes", color="white", fontsize=20)
    
