from subprocess import Popen, PIPE
import time
from events import ProgressCheckerThread


cmd = [
    'python3',
    '-m',
    'image',
    '--class-name',
    'snowboard',
    '--path',
    './data'
]

p = Popen(cmd, stdout=PIPE)

thread = ProgressCheckerThread(p)
thread.start()

while True:
    time.sleep(1)
    if thread.done:
        print('DONE')
        break
    print(f'... {thread.progress}%')

thread.join()
