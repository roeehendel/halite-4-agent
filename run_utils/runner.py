# Set Up Environment

from kaggle_environments import make


class Runner:
    def __init__(self, agents, episode_steps=400):
        self.agents = agents
        self.episode_steps = episode_steps

    def run(self):
        env = make("halite", configuration={"episodeSteps": self.episode_steps, "agentExec": "PROCESS"},
                   debug=True)  # , "agentExec": "PROCESS"
        print(env.configuration)

        # start_time = time.time()
        env.run(self.agents)
        # print('run', time.time() - start_time)

        result = env.render(mode='html', width=800, height=600)

        return result
