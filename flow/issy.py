import json

from flow.core.params import VehicleParams
from flow.core.params import NetParams
from flow.core.params import InitialConfig
from flow.core.params import EnvParams
from flow.core.params import SumoParams
from flow.core.experiment import Experiment
from flow.core.params import TrafficLightParams
from flow.utils.rllib import FlowParamsEncoder

import ray
try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
from ray.tune import run_experiments
from ray.tune.registry import register_env

from IssyEnv import IssyEnv1
from IssyScenario import IssyScenario, EDGES_DISTRIBUTION
from helpers import make_create_env, get_inflow


class IssyExperimentParams:
    def __init__(self,
                 horizon,
                 rollouts,
                 inflow_spec,
                 n_cpus,
                 n_veh,
                 checkpoint_freq=20,
                 training_iteration=200, algorithm="PPO"):
        self.horizon = horizon
        self.rollouts = rollouts
        self.n_cpus = n_cpus
        self.inflow_spec = inflow_spec
        self.n_veh = n_veh
        self.checkpoint_freq = checkpoint_freq
        self.training_iteration = training_iteration
        self.algorithm = algorithm

        self.osm_path = '/home/thomas/sumo/models/issy.osm'
        self.edges_distribution = EDGES_DISTRIBUTION

class IssyExperiment:
    def __init__(self, params):
        self.exp_params = params
        self.flow_params = self.make_flow_params()

        ray.init(num_cpus=self.exp_params.n_cpus + 1, redirect_output=False)

    def run(self):
        alg_run, gym_name, config = 1, 1, 1
        if self.exp_params.algorithm == 'PPO':
            alg_run, gym_name, config = self.setup_ppo_exp()
        else:
            return NotImplementedError

        trials = run_experiments({
            self.flow_params['exp_tag']: {
                'run': alg_run,
                'env': gym_name,
                'config': {
                    **config
                },
                'checkpoint_freq': self.exp_params.checkpoint_freq,
                'max_failures': 999,
                'stop': {
                    'training_iteration': self.exp_params.training_iteration,
                },
            }
        })

    def setup_ppo_exp(self):
        alg_run = 'PPO'

        agent_cls = get_agent_class(alg_run)
        config = agent_cls._default_config.copy()
        config['num_workers'] = self.exp_params.n_cpus
        config['train_batch_size'] = self.exp_params.horizon * self.exp_params.rollouts
        config['gamma'] = 0.999  # discount rate
        config['model'].update({'fcnet_hiddens': [32, 32]})
        config['use_gae'] = True
        config['lambda'] = 0.97
        config['kl_target'] = 0.02
        config['num_sgd_iter'] = 10
        config['clip_actions'] = False  # FIXME(ev) temporary ray bug
        config['horizon'] = self.exp_params.horizon

        # save the flow params for replay
        flow_json = json.dumps(
            self.flow_params,
            cls=FlowParamsEncoder,
            sort_keys=True,
            indent=4)
        config['env_config']['flow_params'] = flow_json
        config['env_config']['run'] = alg_run

        create_env, gym_name = make_create_env(
            params=self.flow_params, version=0)

        # Register as rllib env
        register_env(gym_name, create_env)
        e = create_env()
        return alg_run, gym_name, config

    def make_flow_params(self):
        return dict(
            exp_tag='IssyEnv',
            env_name='IssyEnv1',
            scenario='IssyScenario',
            simulator='traci',
            sim =self.make_sumo_params(),
            env =self.make_env_params(),
            net =self.make_net_params(),
            veh =self.make_vehicles(),
            initial = self.make_initial_config(),
        )

    def make_inflow(self):
        return get_inflow(self.exp_params.inflow_spec)

    def make_vehicles(self):
        vehicles = VehicleParams()
        vehicles.add('human', num_vehicles=self.exp_params.n_veh)
        return vehicles

    def make_net_params(self):
        return NetParams(
            osm_path=self.exp_params.osm_path,
            no_internal_links=False,
            inflows=self.make_inflow(),
        )

    def make_initial_config(self):
        return InitialConfig(
            edges_distribution=self.exp_params.edges_distribution,
        )

    def make_env_params(self):
        return EnvParams(
            additional_params={"beta": self.exp_params.n_veh},
            horizon=self.exp_params.horizon,
            warmup_steps=750,
        )

    def make_sumo_params(self):
        return SumoParams(render=False, restart_instance=True)


if __name__ == '__main__':
    inflow_spec = {
        "N": 300,
        "NW": 150,
        "E": 300,
        "loop": 300,
        "155558218": 150,
    }
    params = IssyExperimentParams(horizon=1000,
                            rollouts=2,
                            inflow_spec=inflow_spec,
                            n_cpus=0,
                            n_veh=20,
                            checkpoint_freq=20,
                            training_iteration=200,
                            algorithm="PPO")

    exp = IssyExperiment(params)
    exp.run()
