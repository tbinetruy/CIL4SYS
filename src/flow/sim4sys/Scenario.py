
"""Script containing the Sim4sys scenario kernel class.

This file derives from a copy paste of `flow.core.kernel.Scenario.traci`."""

from flow.core.kernel.scenario import KernelScenario


class Sim4sysScenario(KernelScenario):
    """Base scenario kernel for sumo-based simulations.

    This class initializes a new scenario. Scenarios are used to specify
    features of a network, including the positions of nodes, properties of the
    edges and junctions connecting these nodes, properties of vehicles and
    traffic lights, and other features as well.
    """

    def __init__(self, master_kernel, sim_params):
        """Instantiate a sumo scenario kernel.

        Parameters
        ----------
        master_kernel : flow.core.kernel.Kernel
            the higher level kernel (used to call methods from other
            sub-kernels)
        sim_params : flow.core.params.SimParams
            simulation-specific parameters
        """
        super(Sim4sysScenario, self).__init__(master_kernel, sim_params)
        pass

    def generate_network(self, network):
        """See parent class.

        Parameters
        ----------
        network : flow.scenarios.Scenario
            an object containing relevant network-specific features such as the
            locations and properties of nodes and edges in the network
        """
        return NotImplementedError

    def update(self, reset):
        """Perform no action of value (scenarios are static)."""
        pass

    def close(self):
        """Close the scenario class.

        Deletes the xml files that were created by the scenario class. This
        is to prevent them from building up in the debug folder. Note that in
        the case of import .net.xml files we do not want to delete them.
        """
        return NotImplementedError

    def get_edge(self, x):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        for (edge, start_pos) in reversed(self.total_edgestarts):
            if x >= start_pos:
                return edge, x - start_pos

    def get_x(self, edge, position):
        """See parent class."""
        return NotImplementedError

    def edge_length(self, edge_id):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        try:
            return self._edges[edge_id]['length']
        except KeyError:
            print('Error in edge length with key', edge_id)
            return -1001

    def length(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__length

    def speed_limit(self, edge_id):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        try:
            return self._edges[edge_id]['speed']
        except KeyError:
            print('Error in speed limit with key', edge_id)
            return -1001

    def num_lanes(self, edge_id):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        try:
            return self._edges[edge_id]['lanes']
        except KeyError:
            print('Error in num lanes with key', edge_id)
            return -1001

    def max_speed(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self.__max_speed

    def get_edge_list(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self._edge_list

    def get_junction_list(self):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        return self._junction_list

    def next_edge(self, edge, lane):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        try:
            return self._connections['next'][edge][lane]
        except KeyError:
            return []

    def prev_edge(self, edge, lane):
        """See parent class.
        Copied from `flow.core.kernel.vehicle.traci`"""
        try:
            return self._connections['prev'][edge][lane]
        except KeyError:
            return []

        return NotImplementedError

    def generate_net_from_osm(self, net_params):
        """Generate .net.xml files from OpenStreetMap files.

        This is accomplished by calling the sumo ``netconvert`` binary. Only
        vehicle roads are included from the networks.

        Parameters
        ----------
        net_params : flow.core.params.NetParams type
            network-specific parameters. Different networks require different
            net_params; see the separate sub-classes for more information.

        Returns
        -------
        edges : dict <dict>
            Key = name of the edge
            Elements = length, lanes, speed
        connection_data : dict < dict < list<tup> > >
            Key = name of the arriving edge
                Key = lane index
                Element = list of edge/lane pairs that a vehicle can traverse
                from the arriving edge/lane pairs
        """
        return NotImplementedError
