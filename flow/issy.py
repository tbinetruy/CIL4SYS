import json

from flow.core.params import VehicleParams
from flow.core.params import NetParams
from flow.core.params import InitialConfig
from flow.core.params import EnvParams
from flow.core.params import SumoParams
from flow.core.experiment import Experiment
from flow.core.params import InFlows
from flow.core.params import TrafficLightParams

import ray
try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
from ray.tune import run_experiments
from ray.tune.registry import register_env

from flow.utils.rllib import FlowParamsEncoder

from IssyEnv import IssyEnv
from IssyScenario import IssyScenario, EDGES_DISTRIBUTION
from helpers import make_create_env

# time horizon of a single rollout
HORIZON = 1000
# number of rollouts per training iteration
N_ROLLOUTS = 2
# number of parallel workers
N_CPUS = 0

def get_inflow(spec):
    inflow = InFlows()
    for k, v in spec.items():
        inflow.add(veh_type="human",
                edge=k,
                vehs_per_hour=v,
                departSpeed=10,
                departLane="random")
    return inflow

inflow_spec = {
    "N": 300,
    "NW": 150,
    "E": 300,
    "loop": 300,
    "155558218": 150,
}
inflow = get_inflow(inflow_spec)
vehicles = VehicleParams()
vehicles.add('human', num_vehicles=20)

flow_params = dict(
    exp_tag='IssyEnv',
    env_name='IssyEnv',
    scenario='IssyScenario',
    simulator='traci',
    sim=SumoParams(render=True, restart_instance=True),
    env=EnvParams(
        additional_params={"model_spec": 1},
        horizon=HORIZON,
        warmup_steps=750,
    ),
    net=NetParams(
        osm_path='/home/thomas/sumo/models/issy.osm',
        no_internal_links=False,
        inflows=inflow,
    ),
    veh=vehicles,
    initial = InitialConfig(
        edges_distribution=EDGES_DISTRIBUTION,
    )
)

def setup_exps():

    alg_run = 'PPO'

    agent_cls = get_agent_class(alg_run)
    config = agent_cls._default_config.copy()
    config['num_workers'] = N_CPUS
    config['train_batch_size'] = HORIZON * N_ROLLOUTS
    config['gamma'] = 0.999  # discount rate
    config['model'].update({'fcnet_hiddens': [32, 32]})
    config['use_gae'] = True
    config['lambda'] = 0.97
    config['kl_target'] = 0.02
    config['num_sgd_iter'] = 10
    config['clip_actions'] = False  # FIXME(ev) temporary ray bug
    config['horizon'] = HORIZON

    # save the flow params for replay
    flow_json = json.dumps(
        flow_params, cls=FlowParamsEncoder, sort_keys=True, indent=4)
    config['env_config']['flow_params'] = flow_json
    config['env_config']['run'] = alg_run

    create_env, gym_name = make_create_env(params=flow_params, version=0)

    # Register as rllib env
    register_env(gym_name, create_env)
    e = create_env()
    return alg_run, gym_name, config


if __name__ == '__main__':
    alg_run, gym_name, config = setup_exps()
    ray.init(num_cpus=N_CPUS + 1, redirect_output=False)
    trials = run_experiments({
        flow_params['exp_tag']: {
            'run': alg_run,
            'env': gym_name,
            'config': {
                **config
            },
            'checkpoint_freq': 20,
            'max_failures': 999,
            'stop': {
                'training_iteration': 200,
            },
        }
    })
