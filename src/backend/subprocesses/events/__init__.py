import threading
import io
import time


class ProgressCheckerThread(threading.Thread):
    def __init__(self, process):
        self.done = False
        self.progress = 0.0
        self.process = process
        self.result = None
        super().__init__()

    def run(self):
        for line in io.TextIOWrapper(iter(self.process.stdout),
                                     encoding='utf-8'):
            time.sleep(1)
            if line.startswith('PROGRESS'):
                status = line.strip().replace('PROGRESS: ', '')
                if status.startswith('DONE'):
                    self.done = True
                    self.progress = 100.0
                    self.result = status.replace('DONE: ', '')
                elif status.startswith('RUNNING'):
                    self.progress = float(status.replace('RUNNING: ', ''))


def update_progress_error(message: str):
    pass


def update_progress_done(message: str):
    print(f'PROGRESS: DONE: {message}', flush=True)


def update_progress(value: float):
    print(f'PROGRESS: RUNNING: {value}', flush=True)
