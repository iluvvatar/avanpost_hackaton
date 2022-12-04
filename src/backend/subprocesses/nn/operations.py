import os
import json
import random


from backend.subprocesses.events import update_progress, update_progress_done

STORAGE_PATH = os.getenv('STORAGE_PATH', '/storage/data')
ORIG_STORAGE_PATH = os.path.join(STORAGE_PATH, 'orig')


def predict_single(muid, filename):
    update_progress_done(
            json.dumps({'label': 'snowboard', 'probability': 1.0}))


def predict(umid, dataset):
    labels = [
        'minibus',
        'pickup',
        'ski',
        'tracktor',
        'truck',
        'horse',
        'mower',
        'showboard',
        'train',
        'unknown',
        'skateboard'
    ]

    results = []
    for filename in os.listdir(dataset):
        results.append({'id': filename, 'label': random.choice(labels)})


    update_progress_done(json.dumps(results))


def retrain(umid, class_name):
    update_progress_done(json.dumps({'umid': 'm666'}))
