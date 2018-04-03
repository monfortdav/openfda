import http.client
import json
#Módulos o librerías para descargarnos info en páginas web de forma más fácil

headers = {'User-Agent': 'http-client'}
#Cabeceras, es un diccionario con clave-valor

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason) #Depuración
estructura_json = r1.read().decode("utf-8")
conn.close()


label = json.loads(estructura_json)
info_medicamento=label['results'][0]

#Obtenemos el id, el propósito y el fabricante del medicamento
print ('ID: ',info_medicamento['id'])
print ('Proposito: ',info_medicamento['purpose'][0])

print ('Fabricante: ',info_medicamento['openfda']['manufacturer_name'][0])
