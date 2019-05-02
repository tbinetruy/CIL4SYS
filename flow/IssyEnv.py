import numpy as np

from gym.spaces.box import Box

from flow.envs import Env

from Rewards import Rewards
from helpers import flatten, pad_list


class IssyEnvAbstract(Env):
    """Abstract class to inherit from. It provides helpers
    used accross models such as a traffic light state inversion method

    Required from env_params:

    * beta: (int) number of vehicles the agent can observe
    * action_spec: (dict<str,[str]>) allowed states for each traffic
        light ID.


    States
        To be defined in child class.

    Actions
        The action space consist of a list of float variables ranging from 0-1
        specifying whether a traffic light is supposed to switch or not.

    Rewards
        To be defined in child class.

    Termination
        A rollout is terminated once the time horizon is reached.
    """

    def __init__(self, env_params, sim_params, scenario, simulator='traci'):
        super().__init__(env_params, sim_params, scenario, simulator)
        beta = env_params.get_additional_param("beta")
        self.action_spec = env_params.get_additional_param("action_spec")
        self.model_params = dict(beta=beta, )
        self.rewards = Rewards(self.k)

    def get_num_traffic_lights(self):
        """Counts the number of traffic lights by summing
        the state string length for each intersection.

        Returns
        -------
        Number of traffic lights (int)"""
        count = 0
        for k in self.action_spec.keys():
            count += len(self.action_spec[k][0])
        return count

    def get_num_actions(self):
        """Calculates the number of possible actions by counting the
        traffic light states based on `self.action_spec`. It counts
        the cardinality of the cartesian product of all traffic light
        states.

        Returns
        -------
        Number of actions (int)
        """
        count = 1
        for k in self.action_spec.keys():
            count *= len(self.action_spec[k])
        return count

    @property
    def action_space(self):
        """Vector of floats from 0-1 indicating traffic light states."""
        return Box(low=0,
                   high=1,
                   shape=(self.get_num_actions(), ),
                   dtype=np.float32)

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

    def _invert_tl_state(self, id, api="sumo"):
        """Invert state for given traffic light.
        It currently only implements conversion for the sumo light state.
        This function returns the new state string (of the same length as the
        input state), this allows for handling intersections with different
        numbers of lanes and lights elegantly.

        This function takes any sumo light state but only convets to a "green"
        or "red" state. Orange and other states are converted accordingly, see
        implementation for more detail.

        Parameters
        ----------
        id: str
            ID of traffic light to invert
            Use `flow.kernel.traffic_light.get_ids` to get a list of traffic
            light ids.
        api: str
            Simulator API which defines the light state format to return.
            Currently only implements the sumo traffic state format.
            (see: https://sumo.dlr.de/wiki/Simulation/Traffic_Lights#Signal_state_definitions)

        Returns
        ----------
        new_state: str
            New light state consisting of only red and green lights that
            oppose the previous state as much as possible.

        """
        if api == "sumo":
            old_state = self.k.traffic_light.get_state(id)
            state = old_state.replace("g", "G")
            state = state.replace("y", "r")
            state = state.replace("G", "tmp")
            state = state.replace("r", "G")
            state = state.replace("tmp", "r")
            return state
        else:
            return NotImplementedError

    def _apply_rl_actions(self, rl_actions):
        """Converts probabilities of switching each lights into actions by
        rounding them. We then invert the traffic lights that the agent
        requested changes for.

        Parameters
        ----------
        rl_actions: [float]
            Individual probabilities of switching traffic light states.
        """
        tl_ids = self.k.traffic_light.get_ids()
        actions = np.round(rl_actions)

        for id, a in zip(tl_ids, actions):
            if a:
                state = self._invert_tl_state(id)
                self.k.traffic_light.set_state(id, state)

    def additional_command(self):
        """Used to insert vehicles that are on the exit edge and place them
        back on their entrance edge."""
        for veh_id in self.k.vehicle.get_ids():
            self._reroute_if_final_edge(veh_id)

    def get_observable_veh_ids(self):
        """Get the ids of all the vehicles observable by the model.

        Returns
        -------
        A list of vehicle ids (str)
        """
        return [id for id in self.k.vehicle.get_ids() if "human" in id]

    def _reroute_if_final_edge(self, veh_id):
        """Checks if an edge is the final edge. If it is spawn a new
        vehicle on a random edge and remove the old one."""

        # no need to reroute inflows
        if "flow" in veh_id:
            return

        # don't reroute if vehicle is not on route final edge
        current_edge = self.k.vehicle.get_edge(veh_id)
        final_edge = self.k.vehicle.get_route(veh_id)[-1]
        if current_edge != final_edge:
            return

        type_id = self.k.vehicle.get_type(veh_id)

        # remove the vehicle
        self.k.vehicle.remove(veh_id)
        # reintroduce it at the start of the network
        random_route = self.scenario.get_random_route()
        self.k.vehicle.add(veh_id=veh_id,
                           edge=random_route,
                           type_id=str(type_id),
                           lane=str(0),
                           pos="0",
                           speed="max")


class IssyEnv1(IssyEnvAbstract):
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
        # tl = [self.k.traffic_light.get_state(t)
        #       for t in self.k.traffic_light.get_ids()]

        # We pad the state in case a vehicle is being respawned to prevent
        # dimension related exceptions
        vel = pad_list(vel, self.model_params["beta"], 0.)
        orientation = pad_list(orientation, self.model_params["beta"],
                               [0., 0., 0.])
        emission = pad_list(emission, self.model_params["beta"], 0.)

        return np.concatenate((flatten(orientation), vel, emission))

    def compute_reward(self, rl_actions, **kwargs):
        """ The reward in this simple model is simply the mean velocity
        of all simulated vehicles present on the mesh devided by the
        mean CO2 emission.

        (See parent class for more information)"""

        return self.rewards.mean_speed() / self.rewards.mean_emission()
