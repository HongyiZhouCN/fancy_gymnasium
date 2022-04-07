import unittest

import gym
import numpy as np

import alr_envs  # noqa
from alr_envs.utils.make_env_helpers import make

ALL_SPECS = list(spec for spec in gym.envs.registry.all() if "alr_envs" in spec.entry_point)
SEED = 1


class TestMPEnvironments(unittest.TestCase):

    def _run_env(self, env_id, iterations=None, seed=SEED, render=False):
        """
        Example for running a DMC based env in the step based setting.
        The env_id has to be specified as `domain_name-task_name` or
        for manipulation tasks as `manipulation-environment_name`

        Args:
            env_id: Either `domain_name-task_name` or `manipulation-environment_name`
            iterations: Number of rollout steps to run
            seed= random seeding
            render: Render the episode

        Returns:

        """
        env: gym.Env = make(env_id, seed=seed)
        rewards = []
        observations = []
        dones = []
        obs = env.reset()
        self._verify_observations(obs, env.observation_space, "reset()")

        length = env.spec.max_episode_steps
        if iterations is None:
            if length is None:
                iterations = 1
            else:
                iterations = length

        # number of samples(multiple environment steps)
        for i in range(iterations):
            observations.append(obs)

            ac = env.action_space.sample()
            # ac = np.random.uniform(env.action_space.low, env.action_space.high, env.action_space.shape)
            obs, reward, done, info = env.step(ac)

            self._verify_observations(obs, env.observation_space, "step()")
            self._verify_reward(reward)
            self._verify_done(done)

            rewards.append(reward)
            dones.append(done)

            if render:
                env.render("human")

            if done:
                obs = env.reset()

        assert done, "Done flag is not True after max episode length."
        observations.append(obs)
        env.close()
        del env
        return np.array(observations), np.array(rewards), np.array(dones)

    def _run_env_determinism(self, ids):
        seed = 0
        for env_id in ids:
            with self.subTest(msg=env_id):
                traj1 = self._run_env(env_id, seed=seed)
                traj2 = self._run_env(env_id, seed=seed)
                for i, time_step in enumerate(zip(*traj1, *traj2)):
                    obs1, rwd1, done1, obs2, rwd2, done2 = time_step
                    self.assertTrue(np.array_equal(obs1, obs2), f"Observations [{i}] {obs1} and {obs2} do not match.")
                    self.assertEqual(rwd1, rwd2, f"Rewards [{i}] {rwd1} and {rwd2} do not match.")
                    self.assertEqual(done1, done2, f"Dones [{i}] {done1} and {done2} do not match.")

    def _verify_observations(self, obs, observation_space, obs_type="reset()"):
        self.assertTrue(observation_space.contains(obs),
                        f"Observation {obs} received from {obs_type} "
                        f"not contained in observation space {observation_space}.")

    def _verify_reward(self, reward):
        self.assertIsInstance(reward, float, f"Returned {reward} as reward, expected float.")

    def _verify_done(self, done):
        self.assertIsInstance(done, bool, f"Returned {done} as done flag, expected bool.")

    def test_alr_environment_functionality(self):
        """Tests that environments runs without errors using random actions for ALR MP envs."""
        with self.subTest(msg="DMP"):
            for env_id in alr_envs.ALL_ALR_MOTION_PRIMITIVE_ENVIRONMENTS['DMP']:
                with self.subTest(msg=env_id):
                    self._run_env(env_id)

        with self.subTest(msg="ProMP"):
            for env_id in alr_envs.ALL_ALR_MOTION_PRIMITIVE_ENVIRONMENTS['ProMP']:
                with self.subTest(msg=env_id):
                    self._run_env(env_id)

    def test_openai_environment_functionality(self):
        """Tests that environments runs without errors using random actions for OpenAI gym MP envs."""
        with self.subTest(msg="DMP"):
            for env_id in alr_envs.ALL_GYM_MOTION_PRIMITIVE_ENVIRONMENTS['DMP']:
                with self.subTest(msg=env_id):
                    self._run_env(env_id)

        with self.subTest(msg="ProMP"):
            for env_id in alr_envs.ALL_GYM_MOTION_PRIMITIVE_ENVIRONMENTS['ProMP']:
                with self.subTest(msg=env_id):
                    self._run_env(env_id)

    def test_dmc_environment_functionality(self):
        """Tests that environments runs without errors using random actions for DMC MP envs."""
        with self.subTest(msg="DMP"):
            for env_id in alr_envs.ALL_DEEPMIND_MOTION_PRIMITIVE_ENVIRONMENTS['DMP']:
                with self.subTest(msg=env_id):
                    self._run_env(env_id)

        with self.subTest(msg="ProMP"):
            for env_id in alr_envs.ALL_DEEPMIND_MOTION_PRIMITIVE_ENVIRONMENTS['ProMP']:
                with self.subTest(msg=env_id):
                    self._run_env(env_id)

    def test_metaworld_environment_functionality(self):
        """Tests that environments runs without errors using random actions for Metaworld MP envs."""
        with self.subTest(msg="DMP"):
            for env_id in alr_envs.ALL_METAWORLD_MOTION_PRIMITIVE_ENVIRONMENTS['DMP']:
                with self.subTest(msg=env_id):
                    self._run_env(env_id)

        with self.subTest(msg="ProMP"):
            for env_id in alr_envs.ALL_METAWORLD_MOTION_PRIMITIVE_ENVIRONMENTS['ProMP']:
                with self.subTest(msg=env_id):
                    self._run_env(env_id)

    def test_alr_environment_determinism(self):
        """Tests that identical seeds produce identical trajectories for ALR MP Envs."""
        with self.subTest(msg="DMP"):
            self._run_env_determinism(alr_envs.ALL_ALR_MOTION_PRIMITIVE_ENVIRONMENTS["DMP"])
        with self.subTest(msg="ProMP"):
            self._run_env_determinism(alr_envs.ALL_ALR_MOTION_PRIMITIVE_ENVIRONMENTS["ProMP"])

    def test_openai_environment_determinism(self):
        """Tests that identical seeds produce identical trajectories for OpenAI gym MP Envs."""
        with self.subTest(msg="DMP"):
            self._run_env_determinism(alr_envs.ALL_GYM_MOTION_PRIMITIVE_ENVIRONMENTS["DMP"])
        with self.subTest(msg="ProMP"):
            self._run_env_determinism(alr_envs.ALL_GYM_MOTION_PRIMITIVE_ENVIRONMENTS["ProMP"])

    def test_dmc_environment_determinism(self):
        """Tests that identical seeds produce identical trajectories for DMC MP Envs."""
        with self.subTest(msg="DMP"):
            self._run_env_determinism(alr_envs.ALL_DEEPMIND_MOTION_PRIMITIVE_ENVIRONMENTS["DMP"])
        with self.subTest(msg="ProMP"):
            self._run_env_determinism(alr_envs.ALL_DEEPMIND_MOTION_PRIMITIVE_ENVIRONMENTS["ProMP"])

    def test_metaworld_environment_determinism(self):
        """Tests that identical seeds produce identical trajectories for Metaworld MP Envs."""
        with self.subTest(msg="DMP"):
            self._run_env_determinism(alr_envs.ALL_METAWORLD_MOTION_PRIMITIVE_ENVIRONMENTS["DMP"])
        with self.subTest(msg="ProMP"):
            self._run_env_determinism(alr_envs.ALL_METAWORLD_MOTION_PRIMITIVE_ENVIRONMENTS["ProMP"])


if __name__ == '__main__':
    unittest.main()