from .beerpong.beerpong import BeerPongEnv, BeerPongEnvStepBasedEpisodicReward
from .hopper_jump.hopper_jump import HopperJumpEnv
from .hopper_jump.hopper_jump_on_box import HopperJumpOnBoxEnv
from .reacher.reacher import ReacherEnv
from .box_pushing.box_pushing_env import BoxPushingDense, BoxPushingTemporalSparse, BoxPushingTemporalSpatialSparse
from .table_tennis.table_tennis_env import TableTennisEnv, TableTennisWind, TableTennisGoalSwitching, TableTennisRandomInit

try:
    from .air_hockey.air_hockey_env_wrapper import AirHockeyEnv
except ModuleNotFoundError:
    print("[FANCY GYM] Air Hockey not available (depends on mushroom-rl, dmc, mujoco)")