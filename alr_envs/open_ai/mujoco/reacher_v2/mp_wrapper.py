from typing import Union

import numpy as np
from mp_env_api import MPEnvWrapper


class MPWrapper(MPEnvWrapper):

    @property
    def current_vel(self) -> Union[float, int, np.ndarray]:
        return self.sim.data.qvel[:2]

    @property
    def current_pos(self) -> Union[float, int, np.ndarray]:
        return self.sim.data.qpos[:2]

    @property
    def dt(self) -> Union[float, int]:
        return self.env.dt