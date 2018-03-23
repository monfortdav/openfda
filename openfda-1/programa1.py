import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
estructura_json = r1.read().decode("utf-8")
conn.close()

#escribimos a fichero lo recibido
#fichero = open ('label.json', 'w')
#fichero.write(label_raw)
#fichero.close()
#fin escribir


label = json.loads(estructura_json)
medicamento_info=label['results'][0]

print ('ID: ',medicamento_info['id'])
print ('Proposito: ',medicamento_info['purpose'][0])

print ('Fabricante: ',medicamento_info['openfda']['manufacturer_name'][0])
