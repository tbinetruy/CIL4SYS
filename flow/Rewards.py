import numpy as np


class Rewards:
    """Class providing rewards as methods allowing for easy composition of
    rewards from the IssyEnvAbstract derived classes."""

    def __init__(self, kernel):
        """Instantiates a Reward object.

        Parameters
        ----------
        kernel: `flow.core.kernel.vehicle.TraCIVehicle`
            The TraCI Flow kernel for interacting with Sumo vehicles."""
        self.kernel = kernel

    def get_ids(self):
        """Returns IDs of vehicles on the map at current time step."""
        return self.kernel.vehicle.get_ids()

    def mean_speed(self):
        """Returns the mean velocity for all vehicles on the simulation."""
        speeds = self.kernel.vehicle.get_speed(self.get_ids())
        return np.mean(speeds)

    def mean_emission(self):
        """Returns the mean CO2 emission for all vehicles on the simulation."""
        emission = [
            self.kernel.vehicle.kernel_api.vehicle.getCO2Emission(id)
            for id in self.get_ids()
        ]

        return np.mean(emission)
