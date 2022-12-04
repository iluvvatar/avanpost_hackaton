import os
from subprocess import Popen, PIPE

from backend.subprocesses.events import ProgressCheckerThread

STORAGE_PATH = os.getenv('STORAGE_PATH')
ORIG_STORAGE_PATH = os.path.join(STORAGE_PATH, 'orig')

Process = {
    'DOWNLOAD_IMAGE': None,
    'PREDICT_SINGLE': None,
    'DOWNLOAD_DATASET': None,
    'PREDICT': None,
    'DOWNLOAD_DATASET_FOR_NEW_CLASS': None,
    'RETRAIN': None
}


def run_subprocess(key, cmd, callback, blocking):
    Process[key] = ProgressCheckerThread(Popen(cmd, stdout=PIPE), callback)
    Process[key].start()
    if blocking:
        Process[key].join()


def download_image(link, callback, blocking):
    cmd = [
        'python3',
        '-m', 'backend.subprocesses.image',
        '--command', 'get_image',
        '--path', STORAGE_PATH,
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


def download_dataset(link, callback, blocking):
    cmd = [
        'python3',
        '-m', 'backend.subprocesses.image',
        '--command', 'get_dataset',
        '--path', STORAGE_PATH,
        '--link', link
    ]
    run_subprocess('DOWNLOAD_DATASET', cmd, callback, blocking)


def predict(umid, dataset, callback, blocking):
    cmd = [
        'python3',
        '-m', 'backend.subprocesses.nn',
        '--command', 'predict',
        '--dataset', dataset,
        '--umid', umid
    ]
    run_subprocess('PREDICT', cmd, callback, blocking)


def download_dataset_for_new_class(class_name, callback, blocking):
    cmd = [
        'python3',
        '-m', 'backend.subprocesses.image',
        '--command', 'get_dataset_for_new_class',
        '--path', ORIG_STORAGE_PATH,
        '--class-name', class_name
    ]
    run_subprocess('DOWNLOAD_DATASET_FOR_NEW_CLASS', cmd, callback, blocking)


def retrain(umid, class_name, callback, blocking):
    cmd = [
        'python3',
        '-m', 'backend.subprocesses.nn',
        '--command', 'retrain',
        '--umid', umid,
        '--class-name', class_name
    ]
    run_subprocess('RETRAIN', cmd, callback, blocking)


def get_meta(key):
    if Process[key] is None:
        return {'status': 'NOT_STARTED', 'percentile': 0.0}

    if Process[key].done:
        return {'status': 'COMPLETED', 'percentile': 100.0}

    return {'status': 'RUNNING', 'percentile': Process[key].progress}


def get_data(key):
    if Process[key] is None:
        return {'message': 'bad request'}

    if not Process[key].done or Process[key].result is None:
        return {}

    return Process[key].result
