

# the TestEnv environment is used to simply simulate the network
#from flow.envs import TestEnv

# the Experiment class is used for running simulations
#from flow.core.experiment import Experiment

# all other imports are standard

import random

from flow.scenarios import Scenario

# we create a new scenario class to specify the expected routes
class IssyScenario(Scenario):

    def get_routes_list(self):
        return list(self.specify_routes({}).keys())

    def get_random_route(self):
        return random.choice(self.get_routes_list())

    def specify_routes(self, net_params):
        return {
            "loop": [
                "4794817",
                "4786972#0",
                "4786972#1",
                "4786972#2",
                "4786965#1",
                "4786965#2",
                "4786965#3",
                "4795729",
                "-352962858#1",
                "4795742#0",
                "4795742#1",
                "4786965#3",
                "4786965#4",
                "4786965#5",
            ],
            "N": [
                "-100822066",
                "-352962858#1",
                "-352962858#0",
                "-4786940#1",
                "-4786940#0",
            ],
            "NW": [
                "4794817",
                "4786972#0",
                "4786972#1",
                "4786972#2",
                "4786972#3",
            ],
            "E": [
                "4783299#0",
                "4783299#1",
                "4783299#2",
                "4783299#3",
                "4783299#4",
                "4783299#5",
                "4783299#6",
                "4786940#0",
                "4786940#1",
                "352962858#0",
                "352962858#1",
                "100822066",
            ],
            "155558218": [
                "155558218",
                "4786940#1",
                "352962858#0",
                "352962858#1",
                "100822066",
            ],

        }




