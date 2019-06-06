import numpy as np

from gym.spaces.box import Box

from BaseIssyEnv import BaseIssyEnv
from helpers import pad_list, flatten


class IssyEnv1(BaseIssyEnv):
    """First environment used to train traffic lights to regulate traffic flow
    for the Issy les Moulineaux district of study.

    Required from env_params: See parent class

    States
        An observation is the set of positions, orientations and speeds of the
        beta observed vehicles and the binary state of each RL controlled
        traffic lights.

    Actions
        See parent class

    Rewards
        The reward is the ratio of the average speed for all vehicles present
        on the mesh over the average of their emissions.

    Termination
        See parent class
    """

    @property
    def observation_space(self):
        """ In this model, we only observe 2D-positions and speed norms of
        the beta observable vehicles in cartesian coordinates, along with
        their orientation, absolute speed and CO2 emission. We also include
        the binary state of all RL controlled traffic lights.

        Ex: If beta=2 and gamma=10 (2 observed cars and 3 RL controlled
        traffic lights), our state lives in $R^{5\times2} U B^10$ where
        B={0,1} is the on/off state each traffic light can take.

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

        tl = np.concatenate(
            [self.encode_tl_state(id) for id in self.get_controlled_tl_ids()])

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


class IssyEnv2(IssyEnv1):
    """The model differs from IssyEnv1 with its reward function."""

    def compute_reward(self, rl_actions, **kwargs):
        """ The reward penalizes slow and/or emitting for the beta observable
        vehicles and traffic light state switches.

        (See parent class for more information)"""
        # km/h
        max_speed = 10
        # mg of CO2 emitted per vehicle during the last timestep
        max_emission = 3000
        # Penalty to add if a traffic light changes
        tl_penalty = 30

        return self.rewards.penalize_min_speed(
            max_speed) + self.rewards.penalize_max_emission(
                max_emission) + self.rewards.penalize_tl_switch(tl_penalty)


class IssyEnv3(IssyEnv2):
    """Third environment used to train traffic lights to regulate traffic flow
    for the Issy les Moulineaux district of study.

    Required from env_params: See parent class

    States
        An observation is the set of positions, orientations, time spend idled,
        and speeds of the beta observed vehicles and the binary state of each
        RL controlled traffic lights.

    Actions
        See parent class

    Rewards
        The reward penalizes slow and/or emitting and/or idle time for the beta
        observable vehicles and traffic light state switches.

    Termination
        See parent class
    """

    @property
    def observation_space(self):
        """ In this model, we only observe 2D-positions and speed norms of
        the beta observable vehicles in cartesian coordinates, along with
        their orientation, absolute speed, CO2 emission and time steps spent
        idled (speed=0). We also include the binary state of all RL controlled
        traffic lights.

        Ex: If beta=2 and gamma=10 (2 observed cars and 3 RL controlled
        traffic lights), our state lives in $R^{6\times2} U B^10$ where
        B={0,1} is the on/off state each traffic light can take.

        (See parent class for more information)"""

        return Box(
            low=0,
            high=float("inf"),
            shape=(6 * self.scenario.vehicles.num_vehicles +
                   self.get_num_traffic_lights(), ),
        )

    def get_state(self, **kwargs):
        """ We request positions, orientations, speeds, emissions and
        idled time steps of the beta observable vehicles.

        (See parent class for more information)"""
        ids = self.get_observable_veh_ids()

        idled = [self.obs_veh_wait_steps[id] for id in ids]
        idled = pad_list(idled, self.model_params["beta"], 0.)

        return np.concatenate((super().get_state(), idled))

    def compute_reward(self, rl_actions, **kwargs):
        """ The reward in this simple model is simply the mean velocity
        of all simulated vehicles present on the mesh devided by the
        mean CO2 emission.

        (See parent class for more information)"""
        base_reward = super().compute_reward(rl_actions)

        idled_max_steps = 300
        idle_reward = self.rewards.penalize_max_wait(self.obs_veh_wait_steps,
                                                     idled_max_steps, 10, -10)

        return base_reward + idle_reward
