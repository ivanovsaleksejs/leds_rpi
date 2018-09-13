import _thread

import globals
import led_lamps
import server

globals.no_debug()

led_lamps.fill((0,0,0))

server.connect()

_thread.start_new_thread(led_lamps.redraw_thread, ())

_thread.start_new_thread(server.server, ())
