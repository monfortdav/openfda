import http.client
import json

headers = {'User-Agent': 'http-client'}

skip_number=0
while True:
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=100&skip="+str(skip_number)+"&search=substance_name:%22ASPIRIN%22", None, headers)

    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    estructura_json = r1.read().decode("utf-8")
    conn.close()

    label = json.loads(estructura_json)
    for i in range (len (label['results'])):
        info_medicamento=label['results'][i]
        print ('ID: ',info_medicamento['id'])
        if (info_medicamento['openfda']):
            print('Fabricante: ', info_medicamento['openfda']['manufacturer_name'][0])
    if (len(label['results'])<100):
         break
    skip_number=skip_number+100