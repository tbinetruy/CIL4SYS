from collections import OrderedDict

from IssyExperiment import IssyExperiment, IssyExperimentParams

if __name__ == '__main__':
    inflow_spec = {
        "N": 300,  # cars per hour
        "NW": 100,
        "E": 100,
        "loop": 100,
        "155558218": 100,
    }

    # numbering from the top counter-clockwise
    action_spec = OrderedDict({
        # The main traffic light, in sumo traffic light state strings
        # dictate the state of each traffic light and are ordered counter
        # clockwise.
        "30677963": [
            "GGGGrrrGGGG",  # allow all traffic on the main way w/ U-turns
            "rrrrGGGrrrr",  # allow only traffic from edge 4794817
        ],
        "30763263": [
            "GGGGGGGGGG",  # allow all traffic on main axis
            "rrrrrrrrrr",  # block all traffic on main axis to unclog elsewhere
        ],
        "30677810": [  # the smallest of all controlled traffic lights
            "GGrr",
            "rrGG",
        ],
    })

    params = IssyExperimentParams(horizon=600,
                                  rollouts=5,
                                  inflow_spec=inflow_spec,
                                  action_spec=action_spec,
                                  n_cpus=0,
                                  n_veh=5,
                                  checkpoint_freq=20,
                                  training_iteration=2000,
                                  env_name='IssyEnv2',
                                  warmup_steps=2000,
                                  algorithm="DQN",
                                  render=False,
                                  osm_path='/Users/adrienly/Documents/Telecom/Cil4Sys/CIL4SYS/flow/issy.osm')

    exp = IssyExperiment(params)
    exp.run()
