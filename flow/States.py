import numpy as np
from helpers import pad_list, flatten


class TrafficLightsStates:
    def __init__(self, kernel):
        self.k = kernel

    def _binary_ohe_tl(self, id):
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

    def binary_state_ohe(self, ids):
        """Encodes traffic light states into a binary vector representation.

        Parameters
        ----------
        ids: List<String>
            List of traffic light ids to encode in state vector.

        Returns
        -------
        encoded_state: List<0|1>
             Encoded traffic light states in same order as `ids`."""
        return np.concatenate([self._binary_ohe_tl(id) for id in ids])

    def wait_steps(self, tl_wait_steps):
        """Returns how many steps each intersection have maintained state for.

        Parameters
        ----------
        tl_wait_steps: `BaseIssyEnv.obs_tl_wait_steps`
             Dictionary encoding current state and timer for each intersection

        Returns
        -------
        encoded_state: List<Int>
             Vector encoding how many steps each intersection has maintained
             traffic light state for.
        """
        return [
            tl_wait_steps[tl_id]['timer'] for tl_id in tl_wait_steps.keys()
        ]


class VehicleStates:
    def __init__(self, kernel, beta):
        self.k = kernel
        self.beta = beta

    def speeds(self, ids):
        """Encodes vehicle speeds into a vector representation.

        Parameters
        ----------
        ids: List<String>
            List of vehicle ids to encode in speeds in vector.

        Returns
        -------
        encoded_state: List<Float>
             Encoded orientations in same order as `ids`."""
        return pad_list([self.k.vehicle.get_speed(veh_id) for veh_id in ids],
                        self.beta)

    def orientations(self, ids):
        """Encodes vehicle orientation into a vector representation.
        The orientation for each vehicle is a 3-vector encoding the
        cartesian x and y coordinates along with an angle.

        Parameters
        ----------
        ids: List<String>
            List of vehicle ids to encode in orientation in vector.

        Returns
        -------
        encoded_state: List<Float> of length `3 * len(ids)`
             Encoded orientations in same order as `ids`."""
        orientations = [
            self.k.vehicle.get_orientation(veh_id) for veh_id in ids
        ]
        return flatten(pad_list(orientations, self.beta, [0., 0., 0.]))

    def CO2_emissions(self, ids):
        """Encodes vehicle CO2 emissions into a vector representation.

        Parameters
        ----------
        ids: List<String>
            List of vehicle ids to encode in state vector.

        Returns
        -------
        encoded_state: List<Float>
             Encoded CO2 emissions in same order as `ids`."""
        return pad_list([
            self.k.vehicle.kernel_api.vehicle.getCO2Emission(id) for id in ids
        ], self.beta)

    def wait_steps(self, veh_wait_steps):
        """Encodes steps vehicles spent idled into a vector representation.

        Parameters
        ----------
        ids: List<String>
            List of vehicle ids to encode in state vector.

        Returns
        -------
        encoded_state: List<Float>
             Encoded wait_steps in same order as `ids`."""
        idled = [veh_wait_steps[id] for id in veh_wait_steps.keys()]
        return pad_list(idled, self.beta, 0.)


class States:
    def __init__(self, kernel, beta):
        self.k = kernel
        self.tl = TrafficLightsStates(kernel)
        self.veh = VehicleStates(kernel, beta)
