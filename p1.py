from pyvis.network import Network
import pandas as pd
import pickle
from pathlib import Path
import urllib
import collections
from tqdm import tqdm
import os
import networkx as nx
import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd
import webbrowser

files = sorted(Path('data').glob('*.pickle'))
data = {}
# for each of the 6 files: open, read & add to the data dictionary
for fn in files:
    with open(fn, 'rb') as f:
        part = pickle.load(f)
    data.update(part)

# a helper function to format urls
def remove_url_shizzle(text):
    return urllib.parse.unquote(text).replace('"', '').replace("'", '')

cleaned = {}
#for every key/value pair in data
for key, value in tqdm(data.items()):
    #let's make a niver to read key
    new_key = remove_url_shizzle(key)
    #set value (a dict) as the values for the new cleaned key
    cleaned[new_key] = value
    #format the 'crosslinks' key
    cleaned[new_key]['crosslinks'] = [remove_url_shizzle(crosslink) for crosslink in value['crosslinks']]
data = cleaned

character_list = pd.read_parquet('data/StarWars_Characters.parquet')['key'].tolist()

def get_crosslink_table(key, n = 30, ignore_keys=[]):
    cl = data[key]['crosslinks']
    result = []
    for link in cl:
        if link in character_list:
            n_cl = len(data[link]['crosslinks'])
            result.append({'key': link, 'n_links': n_cl})
    result = pd.DataFrame(result)
    return result.loc[~result.key.isin(ignore_keys)].sort_values('n_links', ascending=False)['key'].head(n).tolist()
level_colors =  {
    0:'#7A84DD',
    1:"#B15B60", 
    2:'#8ACAE5', 
    3:'#BD9267', 
    4:'#F1A54D', 
    5:'#020104',
}

def add_node(graph, key, level, max_level=2, n_crosslinks=10, ignore_keys=[]):
    label = key.replace('_', ' ')
    char = [{'name': label}]
    textblock = pd.DataFrame(char).to_html(header=False, index=False, columns=['name'])
    G.add_node(
        label,
        title=textblock,
        size=10,
        color=level_colors[level],
        label=label,
    )
    if level < max_level:
        next_nodes = get_crosslink_table(key, n=n_crosslinks, ignore_keys=ignore_keys)
        for next_key in next_nodes:
            add_node(G, next_key, level + 1, max_level=max_level, n_crosslinks=n_crosslinks, ignore_keys=next_nodes + [key] + ignore_keys)
            next_label = next_key.replace('_', ' ')
            G.add_edge(
                label,
                next_label,
                weight=max_level / (1 + level),
                title=label+' -> '+next_label,
                width=1.5,
            )

max_level = 2
n_crosslinks = 15
start_key = 'Anakin_Skywalker'

G = Network(height="1000px", 
width="100%", 
bgcolor="#000000", 
font_color="white",
notebook=True)

add_node(G, start_key, 0, max_level=max_level, n_crosslinks=n_crosslinks)
G.barnes_hut(gravity=-5000, central_gravity=0, spring_length=200, spring_strength=0.009, damping=0.025, overlap=0)

G.show('index.html')