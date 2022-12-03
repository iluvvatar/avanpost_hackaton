import os
import time
from subprocess import Popen, PIPE
from subprocesses.events import ProgressCheckerThread

CUSTOM_PYTHON_PATH = os.getenv('CUSTOM_PYTHON_PATH')
RANDOM_IMAGE_FROM_INTERNET = os.getenv('RANDOM_IMAGE_FROM_INTERNET')

# cmd = [
#     'python3',
#     '-m',
#     'image',
#     '--class-name',
#     'snowboard',
#     '--path',
#     './data'
# ]

cmd = [
    'python3',
    '-m',
    'image',
    '--command',
    'get_image',
    '--path',
    './data',
    '--link',
    RANDOM_IMAGE_FROM_INTERNET
]

custom_env = os.environ.copy()
custom_env['PYTHONPATH'] = CUSTOM_PYTHON_PATH

p = Popen(cmd, stdout=PIPE, env=custom_env)

thread = ProgressCheckerThread(p)
thread.start()

while True:
    time.sleep(1)
    if thread.done:
        print(f'DONE: {thread.result}')
        break
    print(f'... {thread.progress}%')

thread.join()
