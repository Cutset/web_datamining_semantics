import requests
import pandas as pd
import os

cd = os.getcwd()

URL_SERVER = "http://localhost:3030"
URL_DATASET = URL_SERVER+"/final_project"
URL_GRAPHSTORE = URL_DATASET+"/data"
URL_QUERY = URL_DATASET + "/sparql"

def ontology_uploader(file):
    data_ttl = open(file).read()
    res = requests.post(URL_GRAPHSTORE, data=data_ttl, headers={'Content-Type': 'text/turtle'})
    print("req", res)
    if res.status_code != 204:
        res.raise_for_status()
    else:
        print("Status response",res)

def json_uploader(file):
    data_json = open(file).read()
    res = requests.post(URL_GRAPHSTORE, data=data_json, headers={'Content-Type': 'application/ld+json'})
    #checking if the file was uploaded correctly:
    if res.status_code != 204 and res.status_code != 200:
        res.raise_for_status()
    else:
        print("Status response",res,file,"correctly uploaded !")
        
    return res


def CleanDB():
    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ns: <http://www.owl-ontologies.com/unnamed.owl#> 
        DELETE
        {
            ?s ?p ?o
        }
        WHERE
        {
            ?s ?p ?o
        }
    """
    res = requests.post(URL_DATASET, data=query, headers={'Content-type': 'application/sparql-update'})
    
    #checking if the file was uploaded correctly:
    if res.status_code != 204 :
        res.raise_for_status()
    else:
        print("Status response",res)
        print("Dataset correctly cleared !")
    
    return res

def find(query):
    result = requests.post(URL_QUERY, data=query, headers={'Content-type': 'application/sparql-query'})
    
    if result.status_code != 204 :
        result.raise_for_status()
    else:
        print("Status response",result)
        print("Dataset correctly cleared !")

    return result

def query_to_df(query):
    data = find(query).json()
    l = []
    for elem in data["results"]["bindings"]:
        d = {}
        for k,v in elem.items():
            d[k] = v["value"]
        l.append(d)
    return pd.DataFrame(l)

def query_bool(query):
    data = find(query)
    return data.json()["boolean"]

def query_string(query):
    data = find(query)
    return str(data.content).split('\\n')

def main():
    
    CleanDB()

    ontology_uploader(cd+"/ontology/ontology_projet_final.ttl")

    json_uploader(cd+"/data/monuments.jsonld")
    json_uploader(cd+"/data/velo.jsonld") #dynamic values
    json_uploader(cd+"/data/musees.jsonld")
    
main()