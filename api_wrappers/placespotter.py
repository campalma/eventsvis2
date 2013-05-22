# coding=utf-8
import urllib3, simplejson
from lib.incf.countryutils import transformations

URL = "http://query.yahooapis.com/v1/public/yql"

def find_places(content):
  params = {"q": 'SELECT * FROM geo.placemaker WHERE documentContent ="'+content+'" AND documentType="text/plain"',"format": "json", "diagnostics": "true"}
  http = urllib3.PoolManager()
  response = http.request('GET', URL, fields=params)
  json = response.data
  api_result = simplejson.loads(json)
  print json
  return list(get_all(api_result, "name"))

def get_continents_from_countries(countries):
  continents = []
  for country in countries:
    try:
      continents.append(transformations.cn_to_ctn(country))
    except KeyError:
      pass
  return continents

def get_continents_from_text(content):
  return get_continents_from_countries(find_places(content))

def get_all(data, key):
    sub_iter = []
    if isinstance(data, dict):
        if key in data:
            yield data[key]
        sub_iter = data.itervalues()
    if isinstance(data, list):
        sub_iter = data
    for x in sub_iter:
        for y in get_all(x, key):
            yield y

print get_continents_from_text("Chile es un país super bonito. Su capital es Santiago y la lleva. Queda a 100km de la costa donde está Cartagena, Valparaíso, etc. Viva Chile Mierda!")