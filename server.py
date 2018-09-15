import network
import usocket as socket
import ure as re

import globals
import routes

# Connect to wifi
def connect():

    net = network.WLAN(network.STA_IF)

    if not net.isconnected():
        net.active(True)
        net.connect(globals.secrets["ssid"], globals.secrets["password"])
        while not net.isconnected():
            pass

    print(net.ifconfig())

# Parse GET parameters
def qs_parse(qs):

    parameters = {}
    ampersandSplit = qs.split("&")

    for element in ampersandSplit:
        equalSplit = element.split("=")
        parameters[equalSplit[0]] = equalSplit[1] if len(equalSplit) == 2 else equalSplit[0]

    return parameters

# Process GET request
def get(path):

    route = path
    params = []
    pos = path.find('?')
    fname = path

    if pos > -1:
        fname = path[0:pos]
        params = qs_parse(path[pos+1:])

    route = list(filter(lambda x: not x == "", fname.split('/')))

    if not (fname == "" or fname == "/"):
        try:
            f = open('client/' + fname, "r")
            return {"cmd": "static", "content": f.read()}
        except OSError:
            return {"cmd": "get", "route": route, "params": params}
    else:
        f = open('client/index.html', "r")
        return {"cmd": "static", "content": f.read()}

# Socket server
def server(micropython_optimize = False):

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('',80))
    s.listen(5)

    while True:
        try:
            conn,addr=s.accept()
            request=conn.recv(4096)
            print(conn)

            request = re.compile('\r?\n').split(request.decode('utf-8'))
            method,path,protocol = request[0].split()

            response = ""

            parseGet = get(path)

            if parseGet["cmd"] == "static":
                response = parseGet["content"]
            else:
                if parseGet["cmd"] == "get" and parseGet["route"][0] in routes.routes:
                    response = routes.routes[parseGet["route"][0]](parseGet["route"][1:], parseGet["params"])
                    print(response, response == "")
                    if response == "":
                        response = open('client/index.html', 'r').read();

        except ValueError:
            response = open('client/index.html', 'r').read();

        conn.send(response)
        conn.close()
