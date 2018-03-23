import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
estructura_json = r1.read().decode("utf-8")
conn.close()

#escribimos a fichero lo recibido
#fichero = open ('label.json', 'w')
#fichero.write(estructura_json)
#fichero.close()
#fin escribir


label = json.loads(estructura_json)
for i in range (len (label['results'])):
    medicamento_info=label['results'][i]

    print ('ID: ',medicamento_info['id'])