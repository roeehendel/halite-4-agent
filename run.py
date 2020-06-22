from run_utils.runner import Runner

runner = Runner(["builds/submission.py", "random", "random", "random"], episode_steps=120)

result = runner.run()

with open('replays/test_run.html', 'w') as f:
    f.write(result)
