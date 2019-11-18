#!/usr/bin/env python3

# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

# Code generated from SPARQL queries:
# * http://tinyurl.com/y7l9acas
# * https://w.wiki/CJ9

import csv
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?airlineLabel ?IATA_airline_designator ?ICAO_airline_designator ?official_website ?logo_image WHERE {
  ?airline wdt:P31 wd:Q46970.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  OPTIONAL { ?airline wdt:P856 ?official_website. }
  OPTIONAL { ?airline wdt:P154 ?logo_image. }
  OPTIONAL { ?airline wdt:P229 ?IATA_airline_designator. }
  OPTIONAL { ?airline wdt:P230 ?ICAO_airline_designator. }
}
LIMIT 10000
"""

# 
airline_list = [('3char_code', '2char_code', 'name', 'website', 'logo')]

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

# Main
if __name__ == '__main__':
    #
    result_list = get_results (endpoint_url, query)

    for airline in result_list["results"]["bindings"]:
        #
        # print (str(airline))
        
        iata_code = ''
        if 'IATA_airline_designator' in airline:
            iata_code = airline['IATA_airline_designator']['value']
        icao_code = ''
        if 'ICAO_airline_designator' in airline:
            icao_code = airline['ICAO_airline_designator']['value']
        name = ''
        if 'airlineLabel' in airline:
            name = airline['airlineLabel']['value']
        website = ''
        if 'official_website' in airline:
            website = airline['official_website']['value']
        logo = ''
        if 'logo_image' in airline:
            logo = airline['logo_image']['value']

        #
        record_struct = [icao_code, iata_code, name, website, logo]
        airline_list.append (record_struct)

# Write the results into a CSV
with open('../opentraveldata/optd_airlines_websites_wkdt.csv', 'w') as csvfile:
    file_writer = csv.writer (csvfile, delimiter='^')
    for record in airline_list:
        file_writer.writerow (record)

