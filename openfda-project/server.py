import http.server
import http.client
import json
import socketserver
# Nos llega info de openfda en ficheros json y trabajamos en json.loads.
# Usamos el import socket porque la prática va a escuchar en un socket y a implantar un servidor en un socket.
# Los otros dos imports son porque (server) yo voy a ser un servidor y (client) porque yo voy a ser también un cliente de openfda.

PORT=8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    # API: conjunto de utilidades o recursos que nosotros podemos utilizar.
    OPENFDA_API_URL="api.fda.gov"
    OPENFDA_API_EVENT="/drug/label.json"
    OPENFDA_API_DRUG='&search=active_ingredient:'
    OPENFDA_API_COMPANY='&search=openfda.manufacturer_name:'

    # Construye la web de los formularios como un string.
    def get_main_page(self):
        html = """
            <html>
                <head>
                    <title>OpenFDA App</title>
                </head>
                <body>
                    <h1>OpenFDA Client </h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>
                    **************************************************
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    **************************************************
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    **************************************************
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    **************************************************
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                </body>
            </html>
                """
        return html
    def dame_web (self, lista):
        list_html = """
                                <html>
                                    <head>
                                        <title>OpenFDA Cool App</title>
                                    </head>
                                    <body>
                                        <ul>
                            """
        for item in lista:
            list_html += "<li>" + item + "</li>"

        list_html += """
                                        </ul>
                                    </body>
                                </html>
                            """
        return list_html
    def dame_resultados_genericos (self, limit=10):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit="+str(limit))
        print (self.OPENFDA_API_EVENT + "?limit="+str(limit))
        r1 = conn.getresponse()
        data_raw = r1.read().decode("utf8")
        data = json.loads(data_raw)
        resultados = data['results']
        return resultados
    def do_GET(self):
        recurso_list = self.path.split("?")
        if len(recurso_list) > 1:
            params = recurso_list[1]
        else:
            params = ""

        limit = 1

        # Obtener los parametros
        if params:
            parse_limit = params.split("=")
            if parse_limit[0] == "limit":
                limit = int(parse_limit[1])
                print("Limit: {}".format(limit))
        else:
            print("SIN PARAMETROS")




        # Write content as utf-8 data
        if self.path=='/':
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html=self.get_main_page()
            self.wfile.write(bytes(html, "utf8"))
        elif 'listDrugs' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            medicamentos = []
            resultados = self.dame_resultados_genericos(limit)
            for resultado in resultados:
                if ('generic_name' in resultado['openfda']):
                    medicamentos.append (resultado['openfda']['generic_name'][0])
                else:
                    medicamentos.append('Desconocido')
            resultado_html = self.dame_web (medicamentos)

            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'listCompanies' in self.path:
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            companies = []
            resultados = self.dame_resultados_genericos (limit)
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    companies.append (resultado['openfda']['manufacturer_name'][0])
                else:
                    companies.append('Desconocido')
            resultado_html = self.dame_web(companies)

            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'listWarnings' in self.path:
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            warnings = []
            resultados = self.dame_resultados_genericos (limit)
            for resultado in resultados:
                if ('warnings' in resultado):
                    warnings.append (resultado['warnings'][0])
                else:
                    warnings.append('Desconocido')
            resultado_html = self.dame_web(warnings)

            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'searchDrug' in self.path:
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            #Por defecto 10 en este caso, no 1
            limit = 10
            drug=self.path.split('=')[1]

            drugs = []
            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_EVENT + "?limit="+str(limit) + self.OPENFDA_API_DRUG + drug)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            biblioteca_data = json.loads(data)
            events_search_drug = biblioteca_data['results']
            for resultado in events_search_drug:
                if ('generic_name' in resultado['openfda']):
                    drugs.append(resultado['openfda']['generic_name'][0])
                else:
                    drugs.append('Desconocido')

            resultado_html = self.dame_web(drugs)
            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'searchCompany' in self.path:
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Por defecto 10 en este caso, no 1
            limit = 10
            company=self.path.split('=')[1]
            companies = []
            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_EVENT + "?limit=" + str(limit) + self.OPENFDA_API_COMPANY + company)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            biblioteca_data = json.loads(data)
            events_search_company = biblioteca_data['results']

            for event in events_search_company:
                companies.append(event['openfda']['manufacturer_name'][0])
            resultado_html = self.dame_web(companies)
            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'redirect' in self.path:
            print('Mandamos la redireccion a la página principal')
            self.send_response(301)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else: # Si el recurso solicitado no se encuentra en el servidor.
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())
        return


# Para reservar la ip y el puerto donde el servidor va a escuchar. Permite que se renueve el puerto ya usado. Esta instrucción sirve para cambiar el puerto cuando está pillado y poderlo reutilizarlo.
socketserver.TCPServer.allow_reuse_address= True

# Handler: manejador, es una instancia de la clase, sabe responder ante un do get, manejador de http.
# El manejador no está siempre ejecutando. Cada vez que llegue algo al puerto, este se encarga de gestionar la respuesta.
Handler = testHTTPRequestHandler

# Asocia una ip y un puerto al manejador de peticiones. Cuando llegue una petición a la ip y al puerto el programa le dice a nuestro manejador que atienda.
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
# Forever: Es la línea para que empiece a funcionar el programa.
httpd.serve_forever()