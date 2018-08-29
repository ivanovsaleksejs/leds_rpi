import machine, neopixel, time
import _thread


def no_debug():
    import esp
    # this can be run from the REPL as well
    esp.osdebug(None)

def process_thread():
    while process_thread_active:
        for index, strip in enumerate(strip_data):
            if strip["animation_name"] == "blink":
                demo_blink(index, strip["animation_data"]["color"], strip["animation_data"]["speed"])


def redraw_thread():
    while redraw_active:
        start = time.ticks_ms()
        for index, strip in enumerate(strip_data):
            if not strip["redrawn"] and not strip["stopRedraw"]:
                for led_index, color in enumerate(strip["LEDs"]):
                    int_color = (int(color[0]), int(color[1]), int(color[2]))
                    np[int(index * strip_length + led_index)] = int_color
                strip_data[index]["redrawn"] = True
        np.write()
        end = time.ticks_ms()
        if (end - start) < 1000/frame_rate:
            time.sleep_ms(int(1000/frame_rate - (end - start)))

def demo_blink(strip_number, color, time=1000, pulse=False):
    if strip_data[strip_number]["redrawn"]:

        if not "direction" in strip_data[strip_number]["animation_data"]:
            strip_data[strip_number]["animation_data"]["direction"] = False
        direction = strip_data[strip_number]["animation_data"]["direction"]

        if not "quotient" in strip_data[strip_number]["animation_data"]:
            strip_data[strip_number]["animation_data"]["quotient"] = max(color)**(1./(frame_rate*time/2000))
        quotient = strip_data[strip_number]["animation_data"]["quotient"]

        current_color = strip_data[strip_number]["LEDs"][0]
        if current_color == (0, 0, 0):
            current_color = color
        if current_color[0] < 1 and current_color[1] < 1 and current_color[2] < 1:
            direction = True
        if max(current_color) >= max(color):
            direction = False
            current_color = color
        strip_data[strip_number]["animation_data"]["direction"] = direction

        if direction:
            new_color = (current_color[0]*quotient, current_color[1]*quotient, current_color[2]*quotient)
        else:
            new_color = (current_color[0]/float(quotient), current_color[1]/float(quotient), current_color[2]/float(quotient))

        strip_data[strip_number]["LEDs"] = [new_color for _ in range(0, strip_length)]
        strip_data[strip_number]["redrawn"] = False

def demo_server():
    import machine
    import neopixel
    import socket
    import time
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('ssid', 'passwd')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
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
        print("GOT a connection from %s" % str(addr))
        request=conn.recv(1024)
        print("Content %s" % str(request))
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
        np = neopixel.NeoPixel(machine.Pin(26), 150, timing=1)
        if(blink_red_1==6):
            strip_data[0]["reset"] = True
            strip_data[0]["animation_name"] = "blink"
            strip_data[0]["animation_data"] = {"direction": False, "speed": 1000, "color": (242, 2, 74)}
            strip_data[0]["LEDs"] = [(242, 2, 74) for _ in range(0, strip_length)]
        if(blink_green_1==6):
            strip_data[0]["reset"] = True
            strip_data[0]["animation_name"] = "blink"
            strip_data[0]["animation_data"] = {"direction": False, "speed": 1000, "color": (7, 198, 7)}
            strip_data[0]["LEDs"] = [(7, 198, 7) for _ in range(0, strip_length)]
        if(blink_blue_1==6):
            strip_data[0]["reset"] = True
            strip_data[0]["animation_name"] = "blink"
            strip_data[0]["animation_data"] = {"direction": False, "speed": 1000, "color": (9, 44, 198)}
            strip_data[0]["LEDs"] = [(9, 44, 198) for _ in range(0, strip_length)]
        if(blink_red_f1==6):
            strip_data[0]["reset"] = True
            strip_data[0]["animation_name"] = "blink"
            strip_data[0]["animation_data"] = {"direction": False, "speed": 300, "color": (242, 2, 74)}
            strip_data[0]["LEDs"] = [(242, 2, 74) for _ in range(0, strip_length)]
        if(blink_red_2==6):
            strip_data[1]["reset"] = True
            strip_data[1]["animation_name"] = "blink"
            strip_data[1]["animation_data"] = {"direction": False, "speed": 1000, "color": (242, 2, 74)}
            strip_data[1]["LEDs"] = [(242, 2, 74) for _ in range(0, strip_length)]
        if(blink_green_2==6):
            strip_data[1]["reset"] = True
            strip_data[1]["animation_name"] = "blink"
            strip_data[1]["animation_data"] = {"direction": False, "speed": 1000, "color": (7, 198, 7)}
            strip_data[1]["LEDs"] = [(7, 198, 7) for _ in range(0, strip_length)]
        if(blink_blue_2==6):
            strip_data[1]["reset"] = True
            strip_data[1]["animation_name"] = "blink"
            strip_data[1]["animation_data"] = {"direction": False, "speed": 1000, "color": (9, 44, 198)}
            strip_data[1]["LEDs"] = [(9, 44, 198) for _ in range(0, strip_length)]
        if(blink_red_f2==6):
            strip_data[1]["reset"] = True
            strip_data[1]["animation_name"] = "blink"
            strip_data[1]["animation_data"] = {"direction": False, "speed": 300, "color": (242, 2, 74)}
            strip_data[1]["LEDs"] = [(242, 2, 74) for _ in range(0, strip_length)]
        if(stop==6):
            redraw_active = False


        response=html
        conn.send(response)
        conn.close()

no_debug()

frame_rate = 30
strip_count = 2
strip_length = 30

np = neopixel.NeoPixel(machine.Pin(26), strip_count*strip_length, timing=1)
strip_data = [
    {
        "stopRedraw": False,
        "redrawn": False,
        "reset": True,
        "animation_name": "",
        "animation_data": {},
        "LEDs": [(0, 0, 0) for _ in range (0, strip_length)]
    } for _ in range (0, strip_count)
]
redraw_active = True
process_thread_active = True

np.fill((0,0,0))

_thread.start_new_thread(redraw_thread, ())
_thread.start_new_thread(demo_server, ())
_thread.start_new_thread(process_thread, ())
