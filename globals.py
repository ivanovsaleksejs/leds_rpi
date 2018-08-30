import json
import neopixel
import machine

configFile = open('config.json', 'r')
config = json.loads(configFile.read().replace('\n', ''))
configFile.close()

np = neopixel.NeoPixel(machine.Pin(26), config["stripCount"] * config["stripLength"], timing=1)

strip_data = [
    {
        "stopRedraw": False,
        "redrawn": False,
        "reset": True,
        "animation_name": "",
        "animation_data": {},
        "LEDs": [(0, 0, 0) for _ in range (0, config["stripLength"])]
    } for _ in range (0, config["stripCount"])
]

redraw_active = True
process_thread_active = True
