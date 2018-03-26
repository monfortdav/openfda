import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#conn.request("GET", "/drug/label.json?limit=20&search=active_ingredient:%22acetylsalicylic%22", None, headers)
conn.request("GET", "/drug/label.json?limit=20&search=substance_name:%22ASPIRIN%22", None, headers)

r1 = conn.getresponse()
print(r1.status, r1.reason)
estructura_json = r1.read().decode("utf-8")
conn.close()

#escribimos al fichero lo recibido
fichero = open ('label.json', 'w')
fichero.write(estructura_json)
fichero.close()
#fin  escribir


label = json.loads(estructura_json)
for i in range (len (label['results'])):
    medicamento_info=label['results'][i]

    print ('ID: ',medicamento_info['id'])
    if (medicamento_info['openfda']):
        print('Fabricante: ', medicamento_info['openfda']['manufacturer_name'][0])