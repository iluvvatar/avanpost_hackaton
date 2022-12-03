import os
import time
from subprocess import Popen, PIPE
from events import ProgressCheckerThread

CUSTOM_PYTHON_PATH = os.getenv('CUSTOM_PYTHON_PATH')

cmd = [
    'python3',
    '-m',
    'image',
    '--class-name',
    'snowboard',
    '--path',
    './data'
]

custom_env = os.environ.copy()
custom_env['PYTHONPATH'] = CUSTOM_PYTHON_PATH

p = Popen(cmd, stdout=PIPE, env=custom_env)

thread = ProgressCheckerThread(p)
thread.start()

while True:
    time.sleep(1)
    if thread.done:
        print('DONE')
        break
    print(f'... {thread.progress}%')

thread.join()
