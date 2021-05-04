import json
import textstat
import os
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy

### Extract text from all data files ####
def add_zero(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)

#return the season/episode number that exists in the json files
def sep_val(season_num,episode_num):
    return "s" + add_zero(season_num) + "e" + add_zero(episode_num)

def text_clean_up(line):
    # remove non common text characters
    #line = line.replace("-","")
    line = line.replace("/","")
    backslash = r'\n'    # have to use newline to get rid of eol error from backslash alone
    backslash = backslash[0]   
    line = line.replace(backslash,"")
    line = line.replace("-","")
    line = line.replace("  ","")
    line = line.replace("   ","")
    line = line.replace("    ","")
    line = line.replace(" .",".")

    while (line[len(line-1)] == " ") or line[len(line-1)].isalnum():
        if line[len(line-1)] == " ":
            line = line[0:len(line)-1]
        else:
            line += "."

    return line


def extract_text(season_num,episode_num):
    with  open("gotsubtitles/json/season"+str(season_num)+".json") as f:
        dialog_dict = json.load(f)

    sep = sep_val(season_num,episode_num)

    for key in dialog_dict.keys():
        if sep in key.lower():
            break

    selected_episode = dialog_dict[key]
        
    episode_text = ""
    last_line_num = len(selected_episode.keys())

    for line_num in range(1,last_line_num):
        episode_text += selected_episode[str(line_num)] + ". "
    
    # one last text clean up
    episode_text = episode_text.replace(" .",".")
    episode_text = episode_text.replace("..",".")
    return episode_text




if __name__ == "__main__":


    # seasons 1 - 6
    cumul_ep_num = 1
    episode_data = []
    for season in range(1,7):
        for episode in range(1,11):
            episode_text = extract_text(season,episode)
            episode_data.append([season,episode,cumul_ep_num,episode_text])
            cumul_ep_num += 1

    #season 7 
    season = 7
    for episode in range(1,8):
        episode_text = extract_text(season,episode)
        episode_data.append([season,episode,cumul_ep_num,episode_text])
        cumul_ep_num += 1

    # season 8 
    season = 8
    for episode in range(1,7):
        episode_text = ""
        file_name = "gotsubtitles/season8/Game of Thrones8e"+str(episode)+".txt"
        with open(file_name) as f:
            text = f.read()
        episode_text = text.replace("\n", " ")
        episode_data.append([season,episode,cumul_ep_num,episode_text])
        cumul_ep_num += 1

    # for i in range(len(episode_data)):
    #     print("Season " + str(episode_data[i][0]) + " episode " + str(episode_data[i][1]) + " fk: " + str(textstat.flesch_kincaid_grade(episode_data[i][3])))

    # run flesch kinkaid and gunning fog on each episode
    df = DataFrame(episode_data,columns=['season','episode','cumulative_episodes','episode_text'])
    df['fk'] = df.apply(lambda row: textstat.flesch_kincaid_grade(row.episode_text) , axis=1)
    df['fog_scale'] = df.apply(lambda row: textstat.gunning_fog(row.episode_text) , axis=1)
    df['smog'] = df.apply(lambda row: textstat.smog_index(row.episode_text) , axis=1)
    df['ar'] = df.apply(lambda row: textstat.automated_readability_index(row.episode_text) , axis=1)
    df['standard'] = df.apply(lambda row: textstat.text_standard(row.episode_text) , axis=1)
    
    data_df = df[["fk","fog_scale","smog","ar","standard"]]
    data_df.plot()