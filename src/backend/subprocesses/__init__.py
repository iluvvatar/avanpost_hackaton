import os
from subprocess import Popen, PIPE

from backend.subprocesses.events import ProgressCheckerThread

CUSTOM_PYTHON_PATH = os.getenv('CUSTOM_PYTHON_PATH')
RANDOM_IMAGE_FROM_INTERNET = os.getenv('RANDOM_IMAGE_FROM_INTERNET')


class Process:
    DOWNLOAD_IMAGE = None
    PREDICT_SINGLE = None


def download_image(link, callback, non_blocking=True):
    path = './data'
    cmd = [
        'python3',
        '-m', 'image',
        '--command', 'get_image',
        '--path', path,
        '--link', link
    ]

    custom_env = os.environ.copy()
    custom_env['PYTHONPATH'] = CUSTOM_PYTHON_PATH

    Process.DOWNLOAD_IMAGE = ProgressCheckerThread(
            Popen(cmd, stdout=PIPE, env=custom_env), callback)
    Process.DOWNLOAD_IMAGE.start()

    if not non_blocking:
        Process.DOWNLOAD_IMAGE.join()


def predict_single(umid, callback=None, non_blocking=True):
    cmd = [
        'python3',
        '-m', 'nn',
        '--command', 'predict_single',
        '--filename', Process.DOWNLOAD_IMAGE.result['filename'],
        '--umid', umid
    ]

    custom_env = os.environ.copy()
    custom_env['PYTHONPATH'] = CUSTOM_PYTHON_PATH

    Process.PREDICT_SINGLE = ProgressCheckerThread(
            Popen(cmd, stdout=PIPE, env=custom_env), callback)
    Process.PREDICT_SINGLE.start()

    if not non_blocking:
        Process.PREDICT_SINGLE.join()
