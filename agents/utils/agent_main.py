from kaggle_environments.envs.halite.helpers import Board

from agents.agent import Agent

agent = None


def run_step(observation, config):
    global agent

    if agent is None:
        agent = Agent()

    board = Board(observation, config)

    return agent.get_actions(board)
