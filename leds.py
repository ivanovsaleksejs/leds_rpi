import _thread

import globals
import led_lamps
import server

def no_debug():
    import esp
    # this can be run from the REPL as well
    esp.osdebug(None)

no_debug()

globals.np.fill((0,0,0))

_thread.start_new_thread(led_lamps.redraw_thread, ())
_thread.start_new_thread(server.demo_server, ())
