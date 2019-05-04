import numpy as np

from gym.spaces.box import Box

from BaseIssyEnv import BaseIssyEnv
from helpers import pad_list, flatten


class IssyEnv1(BaseIssyEnv):
    """First environment used to train traffic lights to regulate traffic flow
    for the Issy les Moulineaux district of study.

    Required from env_params: See parent class

    States
        An observation is the set of positions and speeds of beta observed
        vehicles

    Actions
        See parent class

    Rewards
        The reward is the average speed of all vehicles present on the mesh.

    Termination
        See parent class
    """

    @property
    def observation_space(self):
        """ In this model, we only observe positions and speeds of
        the beta observable vehicles in cartesian coordinates,
        along with their absolute speed and CO2 emission.

        (See parent class for more information)"""

        return Box(
            low=0,
            high=float("inf"),
            shape=(5 * self.scenario.vehicles.num_vehicles +
                   self.get_num_traffic_lights(), ),
        )

    def encode_tl_state(self, id):
        """Encodes traffic light state.
        Yellow and red states are considered off and all other states
        are considered on.

        "rryGyggrrGGrg" => [0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1]

        See: https://sumo.dlr.de/wiki/Simulation/Traffic_Lights

        Parameters
        ----------
        id: str
            ID of traffic light to encode state.

        Returns
        ----------
        encoded_state: [bool]
            Encoded light state
        """
        state = list(self.k.traffic_light.get_state(id))
        red_lights = list("ry")
        return [0 if s in red_lights else 1 for s in state]

    def get_state(self, **kwargs):
        """ We request positions, orientations, speeds, and emissions
        of observable vehicles.

        (See parent class for more information)"""
        # We select beta observable vehicles and exclude inflows
        ids = self.get_observable_veh_ids()

        vel = [self.k.vehicle.get_speed(veh_id) for veh_id in ids]
        orientation = [
            self.k.vehicle.get_orientation(veh_id) for veh_id in ids
        ]
        emission = [
            self.k.vehicle.kernel_api.vehicle.getCO2Emission(id) for id in ids
        ]

        tl = np.concatenate([
            self.encode_tl_state(id) for id in self.get_controlled_tl_ids()
        ])

        # We pad the state in case a vehicle is being respawned to prevent
        # dimension related exceptions
        vel = pad_list(vel, self.model_params["beta"], 0.)
        orientation = pad_list(orientation, self.model_params["beta"],
                               [0., 0., 0.])
        emission = pad_list(emission, self.model_params["beta"], 0.)

        return np.concatenate((flatten(orientation), vel, emission, tl))

    def compute_reward(self, rl_actions, **kwargs):
        """ The reward in this simple model is simply the mean velocity
        of all simulated vehicles present on the mesh devided by the
        mean CO2 emission.

        (See parent class for more information)"""

        return self.rewards.mean_speed() / self.rewards.mean_emission()
