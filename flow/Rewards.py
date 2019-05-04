import numpy as np


class Rewards:
    """Class providing rewards as methods allowing for easy composition of
    rewards from the IssyEnvAbstract derived classes.

    All public methods return an integer corresponding to the reward calculated
    at that time step."""

    def __init__(self, kernel, action_spec):
        """Instantiates a Reward object.

        Parameters
        ----------
        kernel: `flow.core.kernel.vehicle.TraCIVehicle`
            The TraCI Flow kernel for interacting with Sumo vehicles.
        action_spec: `BaseIssyEnv.action_spec`
            OrderedDict of controlled traffic light IDs with their allowed
            states."""
        self.kernel = kernel
        self.action_spec = action_spec
        self.tl_states = []  # traffic light states

    def _get_veh_ids(self):
        """Returns IDs of vehicles on the map at current time step."""
        return self.kernel.vehicle.get_ids()

    def _get_controlled_tl_ids(self):
        return list(self.action_spec.keys())

    def penalize_min_speed(self, min_speed, reward=1, penalty=0):
        """This rewards the beta vehicles traveling over min_speed.

        Parameters
        ----------
        min_speed: int
            speed above which rewards are assigned
        reward: int
            reward for each vehicles traveling above the min_speed
        penalty: int
             penalty to assign to vehicles traveling under min_speed"""
        return np.sum([
            reward
            if self.kernel.vehicle.get_speed(id) > min_speed else penalty
            for id in self._get_veh_ids()
        ])

    def penalize_tl_switch(self, penatly=10):
        """This reward penalizes when a controlled traffic light switches
        before a minimum amount of time steps.

        Parameters
        ----------
        penalty: int
             penalty to assign to vehicles traveling under min_speed"""
        current_states = [
            self.kernel.traffic_light.get_state(id)
            for id in self._get_controlled_tl_ids()
        ]

        # Return 0 at first time step and set tl_states
        if not len(self.tl_states):
            self.tl_states = current_states
            return 0

        reward = 0
        for i, old_state in enumerate(self.tl_states):
            if old_state is not current_states[i]:
                reward -= penatly

        return reward




    def penalize_max_emission(self, max_emission, reward=1, penalty=0):
        """This rewards the beta vehicles emitting less CO2 than a constraint.

        Parameters
        ----------
        min_emission: int
            emission level (in mg for the last time step, which is what Sumo
            outputs by default) under which rewards are assigned.
        reward: int
            reward for each vehicles emitting less than max_emission.
        penalty: int
             penalty to assign to vehicles traveling under min_speed"""
        return np.sum([
            reward if self.kernel.vehicle.kernel_api.vehicle.getCO2Emission(id)
            < max_emission else penalty for id in self._get_veh_ids()
        ])

    def mean_speed(self):
        """Returns the mean velocity for all vehicles on the simulation."""
        speeds = self.kernel.vehicle.get_speed(self._get_veh_ids())
        return np.mean(speeds)

    def mean_emission(self):
        """Returns the mean CO2 emission for all vehicles on the simulation."""
        emission = [
            self.kernel.vehicle.kernel_api.vehicle.getCO2Emission(id)
            for id in self._get_veh_ids()
        ]

        return np.mean(emission)
