"""Script containing the Sim4Sys simulation kernel class."""

import asyncio
import websockets
import json

from flow.core.kernel.simulation import KernelSimulation


class Sim4sysSimulation(KernelSimulation):
    """Sin4sys simulation kernel.

    Extends flow.core.kernel.simulation.KernelSimulation

    Communication is done with Sim4sys frontend for now over websockets.

    TODO: This will to be ported to a communication with the Sim4sys backend.
    """

    def __init__(self, master_kernel):
        """Instantiate the sumo simulator kernel.

        Parameters
        ----------
        master_kernel : flow.core.kernel.Kernel
            the higher level kernel (used to call methods from other
            sub-kernels)
        """
        KernelSimulation.__init__(self, master_kernel)
        # contains the subprocess.Popen instance used to start traci
        self.sumo_proc = None
        self.current_resp = []
        self.event_loop = asyncio.get_event_loop()
        self.simulator_url = "localhost"
        self.simulator_port = 9002

    def append_current_resp(self, resp):
        """Adds a message to the current response."""
        self.current_resp.append(resp)

    def _flush_current_resp(self):
        """Resets the current message list."""
        self.current_resp = []

    def start_simulation(self, scenario, sim_params):
        """Start a connection to Sim4Sys.

        The Sim4sys simulator awaits for a websocket message on a given port.
        The method 'tricks' the simulator into thinking it is connected to the
        Sim4sys C++ backend."""
        self.current_resp = {
            "version": "2.8",
            "features": "[]"
        }

        # Send inital request to the simulator
        self.simulation_step()

    async def send_ws_msg(self, websocket, message):
        """Sends a message over websockets to the simulator and flushes msg
        list."""
        if self.current_resp is not None:
            async for message in websocket:
                await websocket.send(json.dumps(self.current_resp))
                self._flush_current_resp()

    def simulation_step(self):
        """See parent class."""
        self.event_loop.run_until_complete(
            websockets.serve(self.send_ws_msg,
                             self.simulator_url,
                             self.simulator_port))

    def update(self, reset):
        """See parent class."""
        pass

    def close(self):
        """See parent class."""
        self.event_loop.close()

    def check_collision(self):
        """See parent class."""
        pass
