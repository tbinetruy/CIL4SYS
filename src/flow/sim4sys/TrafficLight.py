from flow.core.kernel.traffic_light import KernelTrafficLight


class Sim4sysTrafficLight(KernelTrafficLight):
    """Sim4sys traffic light kernel.

    Will implements all methods discussed in the base traffic light kernel
    class."""

    def __init__(self,
                 master_kernel):
        """See parent class."""
        KernelTrafficLight.__init__(self, master_kernel)

    def get_state(self):
        """See parent class."""
        pass

    def set_state(self, node_id, new_state, link_index="all"):
        self.master_kernel.simulation.append_current_resp({
            "name": "sentValues",
            "value": [{
                "name": node_id,
                "type": "string",
                "value": [{
                    "name": "state",
                    "value": new_state
                }]
            }]
        })

    def get_ids(self):
        """See parent class."""
        pass
