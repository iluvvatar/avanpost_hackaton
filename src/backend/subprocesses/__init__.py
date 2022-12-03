import os
from subprocess import Popen, PIPE

from backend.subprocesses.events import ProgressCheckerThread


Process = {
    'DOWNLOAD_IMAGE': None,
    'PREDICT_SINGLE': None
}


def run_subprocess(key, cmd, callback, blocking):
    Process[key] = ProgressCheckerThread(Popen(cmd, stdout=PIPE), callback)
    Process[key].start()
    if blocking:
        Process[key].join()


def download_image(link, callback, blocking):
    path = './data'
    cmd = [
        'python3',
        '-m', 'backend.subprocesses.image',
        '--command', 'get_image',
        '--path', path,
        '--link', link
    ]
    run_subprocess('DOWNLOAD_IMAGE', cmd, callback, blocking)


def predict_single(umid, callback, blocking):
    cmd = [
        'python3',
        '-m', 'backend.subprocesses.nn',
        '--command', 'predict_single',
        '--filename', Process['DOWNLOAD_IMAGE'].result['filename'],
        '--umid', umid
    ]
    run_subprocess('PREDICT_SINGLE', cmd, callback, blocking)
