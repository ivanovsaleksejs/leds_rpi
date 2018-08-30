import network
import socket

import globals

def demo_server():

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(globals.config["ssid"], globals.config["password"])
        while not sta_if.isconnected():
            pass
    html='''<!DOCTYPE html>
    <html>
    <head><title>ESP32 LED</title></head>
    <center>
    <form>
    <button name="cmd" value='blink_red_1' type='submit' style="font-size: 4em; margin: 0.1em; padding:  0.3em; background: rgb(242, 2, 74);"> First Blink Red </button>
    <br>
    <button name="cmd" value='blink_green_1' type='submit' style="font-size: 4em; margin: 0.1em; padding:  0.3em; background: rgb(7, 198, 7);"> First Blink Green </button>
    <br>
    <button name="cmd" value='blink_blue_1' type='submit' style="font-size: 4em; margin: 0.1em; padding:  0.3em; background: rgb(9, 44, 198);"> First Blink Blue </button>
    <br>
    <button name="cmd" value='blink_red_f1' type='submit' style="font-size: 4em; margin: 0.1em; padding:  0.3em; background: rgb(242, 2, 74);"> First Blink Red Fast </button>
    <br>
    <button name="cmd" value='blink_red_2' type='submit' style="font-size: 4em; margin: 0.1em; padding:  0.3em; background: rgb(242, 2, 74);"> Second Blink Red </button>
    <br>
    <button name="cmd" value='blink_green_2' type='submit' style="font-size: 4em; margin: 0.1em; padding:  0.3em; background: rgb(7, 198, 7);"> Second Blink Green </button>
    <br>
    <button name="cmd" value='blink_blue_2' type='submit' style="font-size: 4em; margin: 0.1em; padding:  0.3em; background: rgb(9, 44, 198);"> Second Blink Blue </button>
    <br>
    <button name="cmd" value='blink_red_f2' type='submit' style="font-size: 4em; margin: 0.1em; padding:  0.3em; background: rgb(242, 2, 74);"> Second Blink Red Fast </button>
    <br>
    <br>
    <button name="cmd" value='stop' type='submit' style="font-size: 4em; margin: 0.1em; padding:  0.3em;"> Stop </button>
    <br>
    </form>
    </center>
    '''
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('',80))
    s.listen(5)
    while True:
        conn,addr=s.accept()
        request=conn.recv(1024)
        request=str(request)
        blink_red_1   = request.find('/?cmd=blink_red_1')
        blink_green_1 = request.find('/?cmd=blink_green_1')
        blink_blue_1  = request.find('/?cmd=blink_blue_1')
        blink_red_f1  = request.find('/?cmd=blink_red_f1')
        blink_red_2   = request.find('/?cmd=blink_red_2')
        blink_green_2 = request.find('/?cmd=blink_green_2')
        blink_blue_2  = request.find('/?cmd=blink_blue_2')
        blink_red_f2  = request.find('/?cmd=blink_red_f2')
        stop          = request.find('/?cmd=stop')
        if(blink_red_1==6):
            globals.strip_data[0]["reset"] = True
            globals.strip_data[0]["animation_name"] = "blink"
            globals.strip_data[0]["animation_data"] = {"direction": False, "speed": 1000, "color": (242, 2, 74)}
            globals.strip_data[0]["LEDs"] = [(242, 2, 74) for _ in range(0, globals.config["stripLength"])]
        if(blink_green_1==6):
            globals.strip_data[0]["reset"] = True
            globals.strip_data[0]["animation_name"] = "blink"
            globals.strip_data[0]["animation_data"] = {"direction": False, "speed": 1000, "color": (7, 198, 7)}
            globals.strip_data[0]["LEDs"] = [(7, 198, 7) for _ in range(0, globals.config["stripLength"])]
        if(blink_blue_1==6):
            globals.strip_data[0]["reset"] = True
            globals.strip_data[0]["animation_name"] = "blink"
            globals.strip_data[0]["animation_data"] = {"direction": False, "speed": 1000, "color": (9, 44, 198)}
            globals.strip_data[0]["LEDs"] = [(9, 44, 198) for _ in range(0, globals.config["stripLength"])]
        if(blink_red_f1==6):
            globals.strip_data[0]["reset"] = True
            globals.strip_data[0]["animation_name"] = "blink"
            globals.strip_data[0]["animation_data"] = {"direction": False, "speed": 300, "color": (242, 2, 74)}
            globals.strip_data[0]["LEDs"] = [(242, 2, 74) for _ in range(0, globals.config["stripLength"])]
        if(blink_red_2==6):
            globals.strip_data[1]["reset"] = True
            globals.strip_data[1]["animation_name"] = "blink"
            globals.strip_data[1]["animation_data"] = {"direction": False, "speed": 1000, "color": (242, 2, 74)}
            globals.strip_data[1]["LEDs"] = [(242, 2, 74) for _ in range(0, globals.config["stripLength"])]
        if(blink_green_2==6):
            globals.strip_data[1]["reset"] = True
            globals.strip_data[1]["animation_name"] = "blink"
            globals.strip_data[1]["animation_data"] = {"direction": False, "speed": 1000, "color": (7, 198, 7)}
            globals.strip_data[1]["LEDs"] = [(7, 198, 7) for _ in range(0, globals.config["stripLength"])]
        if(blink_blue_2==6):
            globals.strip_data[1]["reset"] = True
            globals.strip_data[1]["animation_name"] = "blink"
            globals.strip_data[1]["animation_data"] = {"direction": False, "speed": 1000, "color": (9, 44, 198)}
            globals.strip_data[1]["LEDs"] = [(9, 44, 198) for _ in range(0, globals.config["stripLength"])]
        if(blink_red_f2==6):
            globals.strip_data[1]["reset"] = True
            globals.strip_data[1]["animation_name"] = "blink"
            globals.strip_data[1]["animation_data"] = {"direction": False, "speed": 300, "color": (242, 2, 74)}
            globals.strip_data[1]["LEDs"] = [(242, 2, 74) for _ in range(0, globals.config["stripLength"])]
        if(stop==6):
            globals.redraw_active = False


        response=html
        conn.send(response)
        conn.close()
