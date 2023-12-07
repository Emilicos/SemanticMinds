from django.shortcuts import render
from django.http import JsonResponse

import requests

# Create your views here.

BASE_URL = "http://localhost:9999/blazegraph/sparql"

def search(request):
    search = request.GET.get('q', '')

    query = f"""
    prefix : <http://semminds.com/data/>
    prefix class:    <http://semminds.com/class/>
    prefix property: <http://semminds.com/property#>

    select ?company_uri ?company_name (GROUP_CONCAT(?keyword;separator=", ") as ?keywords)
    where {{
    {{
        ?company_uri rdf:type class:Company .
        ?company_uri rdfs:label ?company_name .
    }}
    OPTIONAL
    {{
        ?company_uri property:keyword ?keyword .
    }}
    FILTER (contains(lcase(?company_name), lcase("{search}")) || contains(lcase(?keyword), lcase("{search}")))
    }}
    GROUP BY ?company_uri ?company_name
    LIMIT 10
    """

    params = {
        "query": query,
        "format":"json"
    }
    r = requests.post(BASE_URL, params=params).json()
    # print(r)
    # print(query)

    return JsonResponse(r, safe=False)

def item(request, uri):
    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wds: <http://www.wikidata.org/entity/statement/>
    PREFIX wdv: <http://www.wikidata.org/value/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    prefix : <http://semminds.com/data/>
    prefix class:    <http://semminds.com/class/>
    prefix property: <http://semminds.com/property#>
    prefix owl:      <http://www.w3.org/2002/07/owl#>
    PREFIX schema: <http://schema.org/> 

    SELECT DISTINCT *
    WHERE {{
    {{
        ?company_uri rdf:type class:Company .
        ?company_uri rdfs:label ?company_name .
        ?company_uri owl:sameAs ?item .
        FILTER(contains(lcase(?company_name), lcase("{uri}")))
    }}
    {{
        SERVICE <https://query.wikidata.org/sparql> {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". 
                                ?item schema:description ?schema . }} .
        }}
    }}
    }}
    LIMIT 10
    """

    params = {
        "query": query,
        "format":"json"
    }
    r = requests.post(BASE_URL, params=params).json()
    return JsonResponse(r, safe=False)