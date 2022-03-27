import pandas as pd
import json
from urllib.request import urlopen
import os

cd = os.getcwd()

def json_to_jsonld(file, df):
    data = {"@context": {"@vocab": "http://www.owl-ontologies.com/unnamed.owl#"}, "velo": json.loads(df.to_json(orient='records'))}
    with open(file, 'w') as outfile:
        json.dump(data, outfile)


def main_dataloader():
    url = "https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=1.1.0&outputformat=GEOJSON&request=GetFeature&typename=jcd_jcdecaux.jcdvelov&SRSNAME=urn:ogc:def:crs:EPSG::4171"
    response = urlopen(url)
    data_json = json.loads(response.read())
    data_dict = [data_json["features"][i]["properties"] for i in range(len(data_json["features"]))]

    df_raw = pd.DataFrame(data_dict)
    df = df_raw[["address","lat","lng","bike_stands","status","available_bike_stands","available_bikes","availability","number"]]
    df = df.set_axis(["adress_velo","lat_velo","lng_velo","bike_stands","status","available_bike_stands","available_bikes","availability","id_velo"],axis = "columns")
    df["type"] = "station_velo"

    df.to_json(cd+"/data/velo.json")

    json_to_jsonld(cd+"/data/velo.jsonld", df)

