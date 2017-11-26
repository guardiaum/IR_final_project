import json
import requests

pages = ['George_Orwell', 'Neil_Gaiman']

baseurl = 'http://en.wikipedia.org/w/api.php'
my_atts = {}
my_atts['action'] = 'query'
my_atts['prop'] = 'revisions'
my_atts['rvprop'] = 'content'
my_atts['format'] = 'json'

for page in pages:
    my_atts['titles'] = page
    resp = requests.get(baseurl, params=my_atts)
    data = resp.json()
    print(data['query']['pages'])
    #print(data['query'][0]['revisions'][0]['*'])
