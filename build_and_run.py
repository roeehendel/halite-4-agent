import time

import stickytape

from run_utils.runner import Runner

if __name__ == '__main__':
    source_file = 'agents/utils/agent_main.py'
    dest_file = 'builds/submission.py'

    # if len(sys.argv) > 1:
    #     source_file = sys.argv[1]
    # filename = os.path.split(source_file)[-1].split('.')[0]
    # dest_file = 'builds/{}_build.py'.format(filename)

    result = stickytape.script(source_file, ['.'])

    with open(dest_file, 'w') as f:
        f.write(result)

    start_time = time.time()

    # runner = Runner(["builds/submission.py", "builds/submission.py", "builds/submission.py", "builds/submission.py"],
    runner = Runner(["builds/submission.py", "builds/new_1_0.py", 'random', 'random'],
                    episode_steps=200)

    result = runner.run()

    print('Finished in: {} seconds'.format(time.time() - start_time))

    with open('replays/test_run.html', 'w') as f:
        f.write(result)
