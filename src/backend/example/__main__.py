from subprocess import Popen, PIPE
import threading
import time
import io


class ProgressCheckerThread(threading.Thread):
    def __init__(self, process):
        self.done = False
        self.progress = 0.0
        self.process = process
        super().__init__()

    def run(self):
        for line in io.TextIOWrapper(iter(self.process.stdout),
                                     encoding='utf-8'):
            time.sleep(1)
            if line.startswith('PROGRESS'):
                status = line.strip().replace('PROGRESS: ', '')
                if status == 'DONE':
                    self.done = True
                    self.progress = 100.0
                else:
                    self.progress = float(status)


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
