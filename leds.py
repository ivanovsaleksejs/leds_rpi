#!/usr/bin/python3

import board
import neopixel

import globals
import led_lamps
# import server

(config, secrets) = globals.readConf()

stripData = [
    {
        "zone_name": "circle",
        "animation_name": "blink",
        "animation_data": {
            "color": (255,0,0),
            "speed":2000,
            "zoneLength": 21,
            "stripLength": 60
        },
    },
    {
        "zone_name": "positions",
        "animation_name": "blink",
        "animation_data": {
            "color": (255,0,0),
            "speed":2000,
            "zoneLength": 4,
            "stripLength": 60
        },
    }
]

#np = neopixel.NeoPixel(machine.Pin(config["pinLED"]), config["stripCount"] * config["stripLength"], timing=1)
#np = neopixel.NeoPixel(board.D18, config["stripCount"] * config["stripLength"])

#np.fill((0,0,0))

np = type('obj', (object,), {
    "buf": [],
    "order": [1, 0, 2],
    "bpp": 3
})

#server.connect(secrets)

#_thread.start_new_thread(led_lamps.redraw_thread, (np, config, stripData))
led_lamps.redraw_thread(np, config, stripData)

#_thread.start_new_thread(server.server, (config, stripData))
