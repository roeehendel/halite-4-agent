from kaggle_environments.envs.halite.helpers import Board

from agents.distributed_agent import DistributedAgent

agent = None


def run_step(observation, config):
    # print('hello')

    global agent

    if agent is None:
        agent = DistributedAgent()

    board = Board(observation, config)

    return agent.get_actions(board)
