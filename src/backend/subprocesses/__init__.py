import os
from subprocess import Popen, PIPE

from backend.subprocesses.events import ProgressCheckerThread


class Process:
    DOWNLOAD_IMAGE = None
    PREDICT_SINGLE = None


def download_image(link, callback, non_blocking=True):
    path = './data'
    cmd = [
        'python3',
        '-m', 'backend.subprocesses.image',
        '--command', 'get_image',
        '--path', path,
        '--link', link
    ]

    Process.DOWNLOAD_IMAGE = ProgressCheckerThread(
            Popen(cmd, stdout=PIPE), callback)
    Process.DOWNLOAD_IMAGE.start()

    if not non_blocking:
        Process.DOWNLOAD_IMAGE.join()


def predict_single(umid, callback=None, non_blocking=True):
    cmd = [
        'python3',
        '-m', 'backend.subprocesses.nn',
        '--command', 'predict_single',
        '--filename', Process.DOWNLOAD_IMAGE.result['filename'],
        '--umid', umid
    ]

    Process.PREDICT_SINGLE = ProgressCheckerThread(
            Popen(cmd, stdout=PIPE), callback)
    Process.PREDICT_SINGLE.start()

    if not non_blocking:
        Process.PREDICT_SINGLE.join()
