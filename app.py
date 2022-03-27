from flask import Flask, render_template, render_template_string, request, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange
import pandas as pd
import folium
from map import convert_map_to_html, display_map_monument, display_map_museum, display_map_station, join_id_monument, join_id_museum, join_id_velo
from fuseki_manager import *
import os
from velo_data_loader import *

cd = os.getcwd()

app = Flask(__name__)
Bootstrap(app=app)
#Menu(app=app)
app.config["SECRET_KEY"] = "hard to guess string"

@app.route('/')
def index():
    return render_template('base.html')

@app.route("/plottest", methods=["GET"])
def plotView():
    map = folium.Map(location= [45.764043, 4.835659], zoom_start = 13, width = 1200, heigth = 600, controle_scale = True)
    
    map.save('templates/map.html')
    return render_template('image.html')

df_velo = pd.read_csv(cd + r'\data\velo.csv')
df_museum = pd.read_csv(cd + r'\data\musees.csv')
df_monument = pd.read_csv(cd + r'\data\monuments.csv')

df_velo['id_velo'] = df_velo['id_velo'].apply(lambda x: int(x)).copy()

df_velo['lat_velo'] = df_velo['lat_velo'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x).copy()
df_velo['lng_velo'] = df_velo['lng_velo'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x).copy()

df_museum['lat_musee'] = df_museum['lat_musee'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x)
df_museum['lng_musee'] = df_museum['lng_musee'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x)

df_monument['lat_mon'] = df_monument['lat_mon'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x)
df_monument['lng_mon'] = df_monument['lng_mon'].apply(lambda x: float(x.replace(',', '.')) if type(x)==str else x)



@app.route("/query6a", methods=["GET"])
def plot_query_6a(df_velo =df_velo, df_museum=df_museum, df_monument=df_monument):

    map = folium.Map(location= [45.764043, 4.835659], zoom_start = 13, width = 1200, heigth = 600, controle_scale = True)
    df_velo.apply(lambda row: folium.Marker(location=[row.loc['lat_velo'], row.loc['lng_velo']], 
                  popup=str(row.loc['id_velo']) + '\nAddress : ' + row.loc['adress_velo'] + ' Lyon', 
                  tooltip='click', icon=folium.Icon(color='green', icon = 'bicycle', prefix = 'fa')).add_to(map), axis=1)
    df_museum.apply(lambda row: folium.Marker(location=[row.loc['lat_musee'], row.loc['lng_musee']], 
                  popup=row.loc['nom_musee'] + '\nAddress : ' + row.loc['adresse_musee'] + ' ' + str(row.loc['codep_musee']) + ' Lyon', 
                  tooltip='click', icon=folium.Icon(color='yellow', icon = 'building', prefix = 'fa')).add_to(map), axis=1)
    df_monument.apply(lambda row: folium.Marker(location=[row.loc['lat_mon'], row.loc['lng_mon']], 
                  popup=row.loc['nom_mon'], 
                  tooltip='click', icon=folium.Icon(color='blue', icon = 'camera', prefix = 'fa')).add_to(map), axis=1)
    map.save('templates/map.html')
    df = pd.concat([df_velo, df_museum, df_monument])

    return render_template('image.html', phrase="Display all POI\n", pandas=df.to_html(), map=True)


@app.route("/query6b", methods=["GET"])
def plot_query_6b():

    map = folium.Map(location= [45.764043, 4.835659], zoom_start = 13, width = 1200, heigth = 600, controle_scale = True)
    
    query = """PREFIX j.0: <http://www.owl-ontologies.com/unnamed.owl#>
SELECT ?id_velo ?adress_velo WHERE { ?subject j.0:id_velo ?id_velo ; j.0:adress_velo ?adress_velo.}
"""
    print(query_to_df(query))
    map = display_map_station(map, join_id_velo(query_to_df(query), df_velo))

    map.save('templates/map.html')

    return render_template('image.html', phrase="Display all bike stations and their address\n", pandas=query_to_df(query).to_html(), map=True)


@app.route("/query6c", methods=["GET"])
def plot_query_6c():

    map = folium.Map(location= [45.764043, 4.835659], zoom_start = 13, width = 1200, heigth = 600, controle_scale = True)

    query = """PREFIX j.0: <http://www.owl-ontologies.com/unnamed.owl#>
SELECT ?id_musee ?nom_musee WHERE {?subject j.0:id_musee ?id_musee ; j.0:nom_musee ?nom_musee. FILTER regex(?nom_musee,"art")}

"""
    map = display_map_museum(map, join_id_museum(query_to_df(query), df_museum))
    
    map.save('templates/map.html')

    return render_template('image.html', phrase="Display art Museum\n", pandas=query_to_df(query).to_html(), map=True)


@app.route("/query6d", methods=["GET"])
def plot_query_6d():

    map = folium.Map(location= [45.764043, 4.835659], zoom_start = 13, width = 1200, heigth = 600, controle_scale = True)
    
    query = """PREFIX j.0: <http://www.owl-ontologies.com/unnamed.owl#>
SELECT ?id_mon ?nom_mon ?siecle WHERE {?subject j.0:id_mon ?id_mon; j.0:nom_mon ?nom_mon ; j.0:siecle ?siecle. FILTER(13<=?siecle && ?siecle<=16)}
"""
    print("AAA")
    map = display_map_monument(map, join_id_monument(query_to_df(query), df_monument))

    map.save('templates/map.html')

    return render_template('image.html', phrase="Display monuments dated from 13th to 16th century\n", pandas=query_to_df(query).to_html(), map=True)


@app.route("/optional", methods=["GET"])
def plot_optional():

    map = folium.Map(location= [45.764043, 4.835659], zoom_start = 13, width = 1200, heigth = 600, controle_scale = True)
    
    query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX j.0: <http://www.owl-ontologies.com/unnamed.owl#>
SELECT ?id_mon ?nom_mon ?historique ?adresse_mon WHERE {?subject j.0:id_mon ?id_mon; j.0:nom_mon ?nom_mon.
					  OPTIONAL{?subject j.0:historique ?historique} 
					  OPTIONAL{?subject j.0:adresse_mon ?adresse_mon}
					}
"""
    map = display_map_monument(map, join_id_monument(query_to_df(query), df_monument))

    map.save('templates/map.html')

    return render_template('image.html', phrase="Display monuments which have historic or address\n", pandas=query_to_df(query).to_html(), map=True)


@app.route("/altconj", methods=["GET"])
def plot_altconj():

    map = folium.Map(location= [45.764043, 4.835659], zoom_start = 13, width = 1200, heigth = 600, controle_scale = True)
    
    map.save('templates/map.html')
    df = pd.DataFrame({'Food':[4,8,12],'Car':[1,5,9],'Home':[2,6,10]})

    return render_template('image.html', phrase="This one doesn't work\n", pandas=df.to_html(), map=True)


@app.route("/construction", methods=["GET"])
def plot_construction():

    query = "This query doesn't work"
    
    return render_template('image.html', phrase="Display table wich display for bicycle station its number, available places and number of bikes\n", pandas=query.to_html(), map=False)


@app.route("/ask", methods=["GET"])
def plot_ask():

    query = '''PREFIX j.0: <http://www.owl-ontologies.com/unnamed.owl#>
ASK {?subject j.0:nom_mon "Maison Renaissance" ; j.0:historique ?historique}'''

    return render_template('image.html', phrase="Ask if monument 'Maison Renaissance' have an historic or not:                \n\n", pandas=query_bool(query), map=False)


@app.route("/describe", methods=["GET"])
def plot_describe():

    query = '''PREFIX p: <http://www.owl-ontologies.com/unnamed.owl#>
DESCRIBE ?subject WHERE {?subject p:id_velo "10111"}'''

    return render_template('image.html', phrase="Describe bicycle station 10111\n", pandas=query_string(query), map=False)


@app.route('/map')
def map():
    return render_template('map.html')


if __name__ == "__main__":
    # run server
    print(app.url_map)
    main_dataloader() #loading the dynamic data for
    main() # cleaning the DB and uploading the data on fuseki
    app.run(host= "0.0.0.0", port= 5000, debug= True)