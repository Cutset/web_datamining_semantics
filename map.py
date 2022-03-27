#map

import folium
import pandas as pd
import os

map = folium.Map(location= [45.764043, 4.835659], zoom_start = 13, width = 500, heigth = 800, controle_scale = True)
cd = os.getcwd()

df_velo = pd.read_csv(cd+r'\data\velo.csv')
df_museum = pd.read_csv(cd + r'\data\musees.csv')
df_monument = pd.read_csv(cd +r'\data\monuments.csv')

df_velo['id_velo'] = df_velo['id_velo'].apply(lambda x: int(x)).copy()

df_velo['lat_velo'] = df_velo['lat_velo'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x).copy()
df_velo['lng_velo'] = df_velo['lng_velo'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x).copy()

df_museum['lat_musee'] = df_museum['lat_musee'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x)
df_museum['lng_musee'] = df_museum['lng_musee'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x)

df_monument['lat_mon'] = df_monument['lat_mon'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x)
df_monument['lng_mon'] = df_monument['lng_mon'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x)



def join_id_velo(data, df_velo=df_velo):
    list_id = list(data.iloc[:,0])
    list_id_int = [int(i) for i in list_id]
    df_coord = df_velo[df_velo['id_velo'].isin(list_id_int)]
    return df_coord

def join_id_museum(data, df_museum=df_museum):
    list_id = list(data.iloc[:,0])
    df_coord = df_museum[df_museum['id_musee'].isin(list_id)]
    return df_coord

def join_id_monument(data, df_monument=df_monument):
    list_id = list(data.iloc[:,0])
    df_coord = df_monument[df_monument['id_mon'].isin(list_id)]
    return df_coord

def display_map_station(map, data):
    data.apply(lambda row: folium.Marker(location=[row.loc['lat_velo'], row.loc['lng_velo']], 
                  popup=str(row.loc['id_velo']) + '\nAddress : ' + row.loc['adress_velo'] + ' Lyon', 
                  tooltip='click', icon=folium.Icon(color='green', icon = 'bicycle', prefix = 'fa')).add_to(map), axis=1)
    return map

def display_map_museum(map, data):
    data.apply(lambda row: folium.Marker(location=[row.loc['lat_musee'], row.loc['lng_musee']], 
                  popup=row.loc['nom_musee'] + '\nAddress : ' + row.loc['adresse_musee'] + ' ' + str(row.loc['codep_musee']) + ' Lyon', 
                  tooltip='click', icon=folium.Icon(color='yellow', icon = 'building', prefix = 'fa')).add_to(map), axis=1)
    return map

def display_map_monument(map, data):
    data.apply(lambda row: folium.Marker(location=[row.loc['lat_mon'], row.loc['lng_mon']], 
                  popup=row.loc['nom_mon'], 
                  tooltip='click', icon=folium.Icon(color='blue', icon = 'camera', prefix = 'fa')).add_to(map), axis=1)
    return map

def convert_map_to_html(map):
    return map.get_root().render()