
# Web datamining and semantics project - 2022

Sara VIDAL - Constantin TESTU - Chanelle WEA

## Intro

The three datasets that we have chosen are the data of the bicycle stations of Lyon, the list of the monuments of France and the museums of France.

## DATA CLEANING AND IMPORTATION: 

As far as the list of museums and monuments is concerned, we have put a constraint on the fact that the city of these places is Lyon. 
We then wrote a python script to allow us to convert our dataset to jsonld format to be able to import them into fuseki.
We do this upload automatically with a python script using the fuseki api
This script is *fuseki_manager.py*.
We load the bike dataset data dynamically.

We then make our SPARQL queries in fuseki, we do this through a python script (*fuseki_manager.py* again) that will then retrieve the results of our queries and adapt them to make them compatible with our flask so that we can display them on our API. 

## API :

We have made our API on flask. Our API contains a top navigation bar that allows us to navigate between each query and view its results. When the query allows it and it is possible to do so we display a map where the results of our query are displayed as well as a table with the results themselves. If this is not possible, we only display the result, for example in the case of the query *ask* because the result is a boolean.

## INSTRUCTIONS :

To launch our project you must first open fuseki at localhost:3030 by double clicking on the file *fuseki_server.bat* on your computer. Once this is done you need to run the *app.py* script from our repository. Once the flask is launched, you can go to http://192.168.1.15:5000/ to open and explore the GUI.
