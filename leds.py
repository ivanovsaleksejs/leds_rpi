import _thread
import machine
import neopixel

import globals
import led_lamps
# import server

globals.no_debug()

(config, secrets) = globals.readConf()

stripData = [
    {
        "animation_name": "blink",
        "animation_data": {"color": (255,0,0), "speed":2000},
    } for _ in range (0, config["stripCount"])
    #{
    #    "animation_name": "blink",
    #    "animation_data": {"color": (255,0,182), "speed":4000},
    #} for _ in range (0, config["stripCount"])

    
        #{
            #"animation_name": "blinkrng_solid",
            #"animation_data": {"color": (255, 0, 180), "speed": 800}
        #},
        #{
            #"animation_name": "blinkrng_solid",
            #"animation_data": {"color": (255, 128, 0), "speed": 800}
        #},
        #{
            #"animation_name": "blinkrng_solid",
            #"animation_data": {"color": (0, 255, 127), "speed": 800}
        #},
        #{
            #"animation_name": "blinkrng_solid",
            #"animation_data": {"color": (0, 255, 64), "speed": 800}
        #},
        #{
            #"animation_name": "blinkrng_solid",
            #"animation_data": {"color": (0, 48, 255), "speed": 800}
        #},
        #{
            #"animation_name": "blinkrng_solid",
            #"animation_data": {"color": (255, 0, 180), "speed": 800}
        #},
        #{
            #"animation_name": "blinkrng_solid",
            #"animation_data": {"color": (127, 0, 255), "speed": 800}
        #},
        #{
            #"animation_name": "blinkrng_solid",
            #"animation_data": {"color": (64, 255, 0), "speed": 800}
        #},

    #{
    #    "animation_name": "",
    #    "animation_data": {},
    #} for _ in range (0, config["stripCount"])
]

np = neopixel.NeoPixel(machine.Pin(config["pinLED"]), config["stripCount"] * config["stripLength"], timing=1)

np.fill((0,0,0))

#server.connect(secrets)

_thread.start_new_thread(led_lamps.redraw_thread, (np, config, stripData))

#_thread.start_new_thread(server.server, (config, stripData))
