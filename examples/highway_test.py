"""
Example of a multi-lane network with human-driven vehicles.
"""
import logging
from flow.core.params import SumoParams, EnvParams, NetParams, InitialConfig
from flow.controllers.routing_controllers import *
from flow.core.vehicles import Vehicles

from flow.core.experiment import SumoExperiment
from flow.envs.loop_accel import SimpleAccelerationEnvironment
from flow.scenarios.highway.gen import HighwayGenerator
from flow.scenarios.highway.scenario import HighwayScenario
from flow.controllers.car_following_models import *
from flow.controllers.lane_change_controllers import *

logging.basicConfig(level=logging.INFO)

sumo_params = SumoParams(sumo_binary="sumo-gui")

vehicles = Vehicles()
vehicles.add_vehicles(veh_id="idm",
                      acceleration_controller=(IDMController, {}),
                      lane_change_controller=(StaticLaneChanger, {}),
                      routing_controller=(ContinuousRouter, {}),
                      initial_speed=0,
                      num_vehicles=40)

additional_env_params = {"target_velocity": 8}
env_params = EnvParams(additional_params=additional_env_params)

additional_net_params = {"length": 1000, "lanes": 4,
                         "speed_limit": 30}
net_params = NetParams(additional_params=additional_net_params)

initial_config = InitialConfig(spacing="gaussian_additive",
                               lanes_distribution=4)

scenario = HighwayScenario(name="highway",
                           generator_class=HighwayGenerator,
                           vehicles=vehicles,
                           net_params=net_params,
                           initial_config=initial_config)

env = SimpleAccelerationEnvironment(env_params, sumo_params, scenario)

exp = SumoExperiment(env, scenario)

logging.info("Experiment Set Up complete")

exp.run(1, 1500)

exp.env.terminate()
