#!/usr/bin/python3

import board
import neopixel

import globals
import led_lamps
import stripData
# import server

(config, secrets) = globals.readConf()

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
led_lamps.redraw_thread(np, config, stripData.stripData)

#_thread.start_new_thread(server.server, (config, stripData))
