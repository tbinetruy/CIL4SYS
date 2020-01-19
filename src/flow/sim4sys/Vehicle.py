import collections
import warnings

import numpy as np

from flow.core.kernel.vehicle import KernelVehicle


class Sym4sysVehicle(KernelVehicle):
    """Kernel for the Sym4sys vehicle API.

    Extends flow.core.kernel.vehicle.base.KernelVehicle

    This originates from a copy/paste of the Flow TraCI kernel. We copied it
    to give it an initial structure. We chose not to inherit from it makes more
    semantic sense not two and because we anticipate this class to differ
    largely from the TraCI vehicle kernel.
    """

    def __init__(self,
                 master_kernel,
                 sim_params):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        KernelVehicle.__init__(self, master_kernel, sim_params)

        self.__ids = []  # ids of all vehicles
        self.__human_ids = []  # ids of human-driven vehicles
        self.__controlled_ids = []  # ids of flow-controlled vehicles
        self.__controlled_lc_ids = []  # ids of flow lc-controlled vehicles
        self.__rl_ids = []  # ids of rl-controlled vehicles
        self.__observed_ids = []  # ids of the observed vehicles

        # vehicles: Key = Vehicle ID, Value = Dictionary describing the vehicle
        # Ordered dictionary used to keep neural net inputs in order
        self.__vehicles = collections.OrderedDict()

        # create a sumo_observations variable that will carry all information
        # on the state of the vehicles for a given time step
        self.__sumo_obs = {}

        # total number of vehicles in the network
        self.num_vehicles = 0
        # number of rl vehicles in the network
        self.num_rl_vehicles = 0

        # contains the parameters associated with each type of vehicle
        self.type_parameters = {}

        # list of vehicle ids located in each edge in the network
        self._ids_by_edge = dict()

        # number of vehicles that entered the network for every time-step
        self._num_departed = []
        self._departed_ids = []

        # number of vehicles to exit the network for every time-step
        self._num_arrived = []
        self._arrived_ids = []

    def update(self, reset):
        """See parent class."""
        pass

    def remove(self, veh_id):
        """See parent class."""
        pass

    def set_follower(self, veh_id, follower):
        """Set the follower of the specified vehicle.
        Copied from `flow.core.kernel.vehicle.traci`"""
        self.__vehicles[veh_id]["follower"] = follower

    def set_headway(self, veh_id, headway):
        """Set the headway of the specified vehicle.
        Copied from `flow.core.kernel.vehicle.traci`"""
        self.__vehicles[veh_id]["headway"] = headway

    def get_orientation(self, veh_id):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__vehicles[veh_id]["orientation"]

    def get_timestep(self, veh_id):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__vehicles[veh_id]["timestep"]

    def get_timedelta(self, veh_id):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__vehicles[veh_id]["timedelta"]

    def get_type(self, veh_id):
        """Return the type of the vehicle of veh_id.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__vehicles[veh_id]["type"]

    def get_ids(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__ids

    def get_human_ids(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__human_ids

    def get_controlled_ids(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__controlled_ids

    def get_controlled_lc_ids(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__controlled_lc_ids

    def get_rl_ids(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__rl_ids

    def set_observed(self, veh_id):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if veh_id not in self.__observed_ids:
            self.__observed_ids.append(veh_id)

    def remove_observed(self, veh_id):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if veh_id in self.__observed_ids:
            self.__observed_ids.remove(veh_id)

    def get_observed_ids(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__observed_ids

    def get_ids_by_edge(self, edges):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if isinstance(edges, (list, np.ndarray)):
            return sum([self.get_ids_by_edge(edge) for edge in edges], [])
        return self._ids_by_edge.get(edges, []) or []

    def get_inflow_rate(self, time_span):
        """See parent class."""
        pass

    def get_outflow_rate(self, time_span):
        """See parent class."""
        pass

    def get_num_arrived(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if len(self._num_arrived) > 0:
            return self._num_arrived[-1]
        else:
            return 0

    def get_arrived_ids(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if len(self._arrived_ids) > 0:
            return self._arrived_ids[-1]
        else:
            return 0

    def get_departed_ids(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if len(self._departed_ids) > 0:
            return self._departed_ids[-1]
        else:
            return 0

    def get_speed(self, veh_id, error=-1001):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_default_speed(self, veh_id, error=-1001):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_position(self, veh_id, error=-1001):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_edge(self, veh_id, error=""):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_lane(self, veh_id, error=-1001):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_route(self, veh_id, error=list()):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_length(self, veh_id, error=-1001):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_leader(self, veh_id, error=""):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_follower(self, veh_id, error=""):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_headway(self, veh_id, error=-1001):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_last_lc(self, veh_id, error=-1001):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if isinstance(veh_id, (list, np.ndarray)):
            return [self.get_headway(vehID, error) for vehID in veh_id]

        if veh_id not in self.__rl_ids:
            warnings.warn('Vehicle {} is not RL vehicle, "last_lc" term set to'
                          ' {}.'.format(veh_id, error))
            return error
        else:
            return self.__vehicles.get(veh_id, {}).get("headway", error)

    def get_acc_controller(self, veh_id, error=None):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if isinstance(veh_id, (list, np.ndarray)):
            return [self.get_acc_controller(vehID, error) for vehID in veh_id]
        return self.__vehicles.get(veh_id, {}).get("acc_controller", error)

    def get_lane_changing_controller(self, veh_id, error=None):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if isinstance(veh_id, (list, np.ndarray)):
            return [
                self.get_lane_changing_controller(vehID, error)
                for vehID in veh_id
            ]
        return self.__vehicles.get(veh_id, {}).get("lane_changer", error)

    def get_routing_controller(self, veh_id, error=None):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if isinstance(veh_id, (list, np.ndarray)):
            return [
                self.get_routing_controller(vehID, error) for vehID in veh_id
            ]
        return self.__vehicles.get(veh_id, {}).get("router", error)

    def set_lane_headways(self, veh_id, lane_headways):
        """Set the lane headways of the specified vehicle.
        Copied from `flow.core.kernel.vehicle.traci`"""
        self.__vehicles[veh_id]["lane_headways"] = lane_headways

    def get_lane_headways(self, veh_id, error=list()):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if isinstance(veh_id, (list, np.ndarray)):
            return [self.get_lane_headways(vehID, error) for vehID in veh_id]
        return self.__vehicles.get(veh_id, {}).get("lane_headways", error)

    def get_lane_leaders_speed(self, veh_id, error=list()):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        lane_leaders = self.get_lane_leaders(veh_id)
        return [0 if lane_leader == '' else self.get_speed(lane_leader)
                for lane_leader in lane_leaders]

    def get_lane_followers_speed(self, veh_id, error=list()):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        lane_followers = self.get_lane_followers(veh_id)
        return [0 if lane_follower == '' else self.get_speed(lane_follower)
                for lane_follower in lane_followers]

    def set_lane_leaders(self, veh_id, lane_leaders):
        """Set the lane leaders of the specified vehicle.
        Copied from `flow.core.kernel.vehicle.traci`"""
        self.__vehicles[veh_id]["lane_leaders"] = lane_leaders

    def get_lane_leaders(self, veh_id, error=list()):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if isinstance(veh_id, (list, np.ndarray)):
            return [self.get_lane_leaders(vehID, error) for vehID in veh_id]
        return self.__vehicles[veh_id]["lane_leaders"]

    def set_lane_tailways(self, veh_id, lane_tailways):
        """Set the lane tailways of the specified vehicle.
        Copied from `flow.core.kernel.vehicle.traci`"""
        self.__vehicles[veh_id]["lane_tailways"] = lane_tailways

    def get_lane_tailways(self, veh_id, error=list()):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if isinstance(veh_id, (list, np.ndarray)):
            return [self.get_lane_tailways(vehID, error) for vehID in veh_id]
        return self.__vehicles.get(veh_id, {}).get("lane_tailways", error)

    def set_lane_followers(self, veh_id, lane_followers):
        """Set the lane followers of the specified vehicle.
        Copied from `flow.core.kernel.vehicle.traci`"""
        self.__vehicles[veh_id]["lane_followers"] = lane_followers

    def get_lane_followers(self, veh_id, error=list()):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        if isinstance(veh_id, (list, np.ndarray)):
            return [self.get_lane_followers(vehID, error) for vehID in veh_id]
        return self.__vehicles.get(veh_id, {}).get("lane_followers", error)

    def apply_acceleration(self, veh_ids, acc):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def apply_lane_change(self, veh_ids, direction):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def choose_routes(self, veh_ids, route_choices):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_x_by_id(self, veh_id):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def update_vehicle_colors(self):
        pass

    def get_color(self, veh_id):
        pass

    def set_color(self, veh_id, color):
        pass

    def add(self, veh_id, type_id, edge, pos, lane, speed):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def get_max_speed(self, veh_id, error=-1001):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError

    def set_max_speed(self, veh_id, max_speed):
        """See parent class.

        TODO: implement"""
        raise NotImplementedError
