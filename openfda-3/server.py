import http.server
import socketserver
import http.client
import json

#Puerto donde lanzamos el servidor
PORT = 8006

def dame_lista():
    lista = []
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=10", None, headers)

    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    estructura_json = r1.read().decode("utf-8")
    conn.close()

    label = json.loads(estructura_json)
    for i in range(len(label['results'])):
        info_medicamento = label['results'][i]
        if (info_medicamento['openfda']):
            print('Fabricante: ', info_medicamento['openfda']['generic_name'][0])
            lista.append(info_medicamento['openfda']['generic_name'][0])

    return lista
# Clase con nuestro manejador. Es una clase derivada de BaseHTTPRequestHandler
# Esto significa que "hereda" todos los metodos de esta clase. Y los que
# nosotros consideremos los podemos reemplazar por los nuestros
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET. Este metodo se invoca automaticamente cada vez que hay una
    # peticion GET por HTTP. El recurso que nos solicitan se encuentra
    # en self.path
    def do_GET(self):
        # La primera linea del mensaje de respuesta es el
        # status. Indicamos que OK
        self.send_response(200)

        # En las siguientes lineas de la respuesta colocamos las
        # cabeceras necesarias para que el cliente entienda el
        # contenido que le enviamos (que sera HTML)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content="<html><body style='background-color:purple'><h1>MEDICAMENTOS:</h2>"
        lista=dame_lista ()
        for e in lista:
            content += e+"<br>"
        content+="</body></html>"

        self.wfile.write(bytes(content, "utf8"))
        return


# El servidor comienza a aqui
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")