import _thread
import machine
import neopixel

import globals
import led_lamps
import server

globals.no_debug()

(config, secrets) = globals.readConf()

stripData = [
    {
        "animation_name": "",
        "animation_data": {},
    } for _ in range (0, config["stripCount"])
]

np = neopixel.NeoPixel(machine.Pin(26), config["stripCount"] * config["stripLength"], timing=1)

np.fill((0,0,0))

server.connect(secrets)

_thread.start_new_thread(led_lamps.redraw_thread, (np, config, stripData))

_thread.start_new_thread(server.server, (np, config, stripData))
