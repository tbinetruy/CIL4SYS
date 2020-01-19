from collections import OrderedDict

from IssyExperiment import IssyExperiment, IssyExperimentParams, \
    RayClusterParams

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

    cluster_params = RayClusterParams(use_cluster=False, redis_address="")

    params = IssyExperimentParams(horizon=3000,
                                  rollouts=1,
                                  inflow_spec=inflow_spec,
                                  action_spec=action_spec,
                                  n_cpus=1,
                                  n_veh=5,
                                  cluster_params=cluster_params,
                                  checkpoint_freq=20,
                                  training_iteration=2000,
                                  discount_rate=0.9999999,
                                  env_name='IssyEnv1',
                                  algorithm="DQN",
                                  warmup_steps=500,
                                  render=False,
                                  tl_constraint=[100, 600],  # steps
                                  sim_step=0.1,       # seconds / steps
                                  osm_path='/host/src/flow/issy.osm')

    exp = IssyExperiment(params)
    exp.run()
