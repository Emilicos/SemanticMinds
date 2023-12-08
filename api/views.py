from django.http import JsonResponse
import requests

from semanticminds.settings import BACKEND_API_URL

# Create your views here.

# BASE_URL = "http://35.225.49.109:80/blazegraph/namespace/kb/sparql"
# BASE_URL = "http://localhost:9999/blazegraph/namespace/kb/sparql"
BASE_URL = BACKEND_API_URL
# Getting search result with format
# <BASE-URL>/search/?q=<KEYWORD>&page=<NO-OF-PAGE>
def search(request):
    search = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    limit = 10
    offset = (int(page) - 1) * limit
    
    query = f"""
    prefix :         <http://semminds.com/data/>
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
    LIMIT {limit} OFFSET {offset}
    """

    params = {
        "query": query,
        "format":"json"
    }

    r = requests.post(BASE_URL, params=params).json()
    
    # Currently still havent found the best way to do this, but this works for now (pagination related)
    
    pagination_query = f"""
    prefix :         <http://semminds.com/data/>
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
    """

    pagination_params = {
        "query": pagination_query,
        "format":"json"
    }
    
    r_pagination = requests.post(BASE_URL, params=pagination_params).json()
    
    # print(r)
    # print(query)
    
    total = len(r_pagination["results"]["bindings"])
    
    return JsonResponse({
        "data": r["results"]["bindings"],
        "pagination": {
            "total": total,
            "current_page": int(page),
            "per_page": limit,
            "last_page": int(total / limit) + 1,
        }
    }, safe=False)


# Connect local data with remote data with format
# <BASE-URL>/data/<LOCAL-ITEM-URI>/
def item(request, uri):
    query = f"""
    prefix : 		 <http://semminds.com/data/>
    prefix class:    <http://semminds.com/class/>
    prefix owl:      <http://www.w3.org/2002/07/owl#>
    prefix property: <http://semminds.com/property#>
    PREFIX schema: 	 <http://schema.org/> 
    PREFIX wd: 		 <http://www.wikidata.org/entity/>
    PREFIX wds:		 <http://www.wikidata.org/entity/statement/>
    PREFIX wdt: 	 <http://www.wikidata.org/prop/direct/>
    PREFIX wdv: 	 <http://www.wikidata.org/value/>
    PREFIX wikibase: <http://wikiba.se/ontology#>

    SELECT *
    WHERE {{
    {{
        {{ 
            SELECT ?company_name (GROUP_CONCAT(?investor_name;separator=", ") as ?investors_name) 
            WHERE
            {{
                :{uri} rdf:type class:Company ;
                        rdfs:label ?company_name .
                OPTIONAL {{
                    :{uri} property:investors ?investor_uri .
                    ?investor_uri rdfs:label  ?investor_name .
                }}
            }}
            GROUP BY ?company_name
        }}
        OPTIONAL {{ :{uri} owl:sameAs ?item_uri . }}
        OPTIONAL {{ :{uri} property:valuation ?valuation . }}
        OPTIONAL {{ :{uri} property:url ?url . }}
        OPTIONAL {{ :{uri} property:total_funding ?funding . }}
        OPTIONAL {{ :{uri} property:state ?state . }}
        OPTIONAL {{ :{uri} property:product_url ?product_url . }}
        OPTIONAL {{ :{uri} property:previous_ranking ?rangking . }}
        OPTIONAL {{ :{uri} property:linkedin_url ?linkedin . }}
        OPTIONAL {{ :{uri} property:job_openings ?job_opening . }}
        OPTIONAL {{ :{uri} property:industry ?industry . }}
        OPTIONAL {{ :{uri} property:indeed_url ?indeed_url . }}
        OPTIONAL {{ :{uri} property:growjo_ranking ?growjo_rank . }}
        OPTIONAL {{ :{uri} property:growth_percentage ?growjo_percentage . }}
        OPTIONAL {{ :{uri} property:founded ?year_founded . }}
        OPTIONAL {{ :{uri} property:estimated_revenues ?estimated_reveunes . }}
        OPTIONAL {{ :{uri} property:employees ?employee . }}
        OPTIONAL {{
            {{
                :{uri} property:city ?city_uri .
                ?city_uri rdfs:label  ?city_name .
            }} OPTIONAL {{
                ?city_uri owl:sameAs ?city_wiki .
            }}
        }}
        OPTIONAL {{
            {{
                :{uri} property:country ?country_uri .
                ?country_uri rdfs:label  ?country_name .
            }} OPTIONAL {{
                ?country_uri owl:sameAs ?country_wiki .
            }}  
        }}
    }}
    OPTIONAL
    {{
        SELECT ?item_uri ?description ?instance ?works (GROUP_CONCAT(?founded;separator=", ") as ?founders)
        WHERE {{
        {{
            SELECT ?item_uri ?description ?instance (GROUP_CONCAT(?work;separator=", ") as ?works)
            WHERE {{
                :{uri} owl:sameAs ?item_uri .
                {{
                    SERVICE <https://query.wikidata.org/sparql> {{
                    {{
                        SERVICE wikibase:label
                        {{ bd:serviceParam wikibase:language "en".
                        ?item_uri schema:description ?description . 
                        }}
                    }} OPTIONAL
                    {{
                        ?item_uri wdt:P31 ?instance_wiki .
                        SERVICE wikibase:label
                        {{ bd:serviceParam wikibase:language "en".
                        ?instance_wiki rdfs:label ?instance . 
                        }}
                    }} OPTIONAL
                    {{
                        ?item_uri wdt:P800 ?works_wiki .
                        SERVICE wikibase:label
                        {{ bd:serviceParam wikibase:language "en".
                        ?works_wiki rdfs:label ?work .
                        }}
                    }}

                    }}
                }}
            }}
            GROUP BY ?item_uri ?description ?instance
        }} OPTIONAL
        {{
            :{uri} owl:sameAs ?item_uri .
            SERVICE <https://query.wikidata.org/sparql> {{
                ?item_uri wdt:P112 ?founded_wiki .
                SERVICE wikibase:label
                {{ bd:serviceParam wikibase:language "en".
                ?founded_wiki rdfs:label ?founded .
                }}
            }}
        }}
        }}
        GROUP BY ?item_uri ?description ?instance ?works
    }}
    }}
    """

    params = {
        "query": query,
        "format":"json"
    }

    r = requests.post(BASE_URL, params=params).json()
    return JsonResponse(r["results"]["bindings"], safe=False)