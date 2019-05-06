import itertools
import numpy as np

from gym.spaces.box import Box
from gym.spaces.discrete import Discrete

from flow.envs import Env

from Rewards import Rewards


class BaseIssyEnv(Env):
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
        self.algorithm = env_params.get_additional_param("algorithm")
        self.model_params = dict(beta=beta, )
        self.rewards = Rewards(self.k, self.action_spec)

        # Used for debug purposes
        self.current_timestep = 0

    def map_action_to_tl_states(self, rl_actions):
        """Maps an rl_action list to new traffic light states based on
        `action_spec` or keeps current traffic light states as they are.

        Parameters
        ---------
        rl_actions: [float] list of action probabilities of cardinality
            `self.get_num_actions()`
        """
        identity_action = [tuple(
            self.k.traffic_light.get_state(id)
            for id in self.action_spec.keys()
        )]
        all_actions = list(itertools.product(
            *list(self.action_spec.values()))) + identity_action
        return all_actions[rl_actions]

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
        states. In the DQN case, it also adds 1 to that product to account
        for the "identity" action which keeps the traffic light states as they
        were in the last timestep.

        Returns
        -------
        Number of actions (int)
        """
        count = 1
        for k in self.action_spec.keys():
            count *= len(self.action_spec[k])
        if self.algorithm == "DQN":
            return count + 1
        elif self.algorithm == "PPO":
            return count
        else:
            return NotImplementedError

    @property
    def action_space(self):
        """Vector of floats from 0-1 indicating traffic light states."""
        if self.algorithm == "DQN":
            return Discrete(self.get_num_actions())
        elif self.algorithm == "PPO":
            return Box(low=0,
                       high=1,
                       shape=(self.get_num_actions(), ),
                       dtype=np.float32)
        else:
            return NotImplementedError

    def get_controlled_tl_ids(self):
        """Returns the list of RL controlled traffic lights."""
        return [
            id for id in self.k.traffic_light.get_ids()
            if id in self.action_spec.keys()
        ]

    def get_free_tl_ids(self):
        """Returns the list of uncontrollable traffic lights."""
        return [
            id for id in self.k.traffic_light.get_ids()
            if id not in self.action_spec.keys()
        ]

    def _apply_rl_actions(self, rl_actions):
        """Converts probabilities of choosing configuration for states of
        traffic lights on the map. All traffic lights for which IDs are not
        keys of `self.action_spec` are updated to all green light states.

        Parameters
        ----------
        rl_actions: [float]
            Individual probabilities of choosing a particular traffic
            light state configuration for controllable traffic lights on
            the map.
        """
        # Upadate controllable traffic lights
        new_tl_states = self.map_action_to_tl_states(rl_actions)
        for counter, tl_id in enumerate(self.action_spec.keys()):
            self.k.traffic_light.set_state(tl_id, new_tl_states[counter])

        # Set all other traffic lights to green
        free_tl_ids = self.get_free_tl_ids()
        for tl_id in free_tl_ids:
            old_state = self.k.traffic_light.get_state(tl_id)
            new_state = "G" * len(old_state)
            self.k.traffic_light.set_state(tl_id, new_state)

    def additional_command(self):
        """Used to insert vehicles that are on the exit edge and place them
        back on their entrance edge. Gets executed at each time step.

        See parent class for more information."""
        for veh_id in self.k.vehicle.get_ids():
            self._reroute_if_final_edge(veh_id)

        # Used for debug purposes
        self.current_timestep += 1

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
