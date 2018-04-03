import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
estructura_json = r1.read().decode("utf-8")
conn.close()


label = json.loads(estructura_json)
for i in range (len (label['results'])):
    info_medicamento=label['results'][i]

    print ('ID: ',info_medicamento['id'])
