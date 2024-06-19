import pandas as pd
import numpy as np


statdict = {
    'Demiryurt Station' : 'DEM', 
    'Arıkören Station' : 'ARI', 
    'Karaman Station' : 'KAR', 
    'Kaşınhanı Station':  'KAS', 
    'Çumra Station': 'CUM',
    'Test Station': 'TEST',
    'Bilkent Station': 'BIL'
    }
    
def create_all_tracks(selected_station): 
    statdict = {
        'Demiryurt Station' : 'DEM', 
        'Arıkören Station' : 'ARI', 
        'Karaman Station' : 'KAR', 
        'Kaşınhanı Station':  'KAS', 
        'Çumra Station': 'CUM',
        'Test Station': 'TEST',
        'Bilkent Station': 'BIL'
        }
    tracks_list = {}
    track_points = pd.read_csv(r"/Users/efetarhan/Desktop/Savronik/GUI/data/last_test3.csv",sep=';')
    #track_points = pd.read_csv(r"data/last.csv",sep=';')
    track_points = track_points[track_points['source_station'] == statdict[selected_station]]
    for i in track_points['source'].to_list():
        for j in track_points[track_points['source'] == i]['destination'].to_list():
            rows_with_i_and_j = (track_points['source'] == i) & (track_points['destination'] == j)
            tracks_list[i+'-'+j] = [[track_points[rows_with_i_and_j]['source_X'].item(),track_points[rows_with_i_and_j]['source_Y'].item()],[track_points[rows_with_i_and_j]['destination_X'].item(),track_points[rows_with_i_and_j]['destination_Y'].item()]]

    return tracks_list