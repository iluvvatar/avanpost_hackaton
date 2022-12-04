import os
import json
import random

from ml.ml_megascript import *
from backend.subprocesses.events import update_progress, update_progress_done

STORAGE_PATH = os.getenv('STORAGE_PATH', '/storage/data')
ORIG_STORAGE_PATH = os.path.join(STORAGE_PATH, 'orig')

MAX_EPOCHS = 150
USE_GPU = True
ESR = 5
batch_size = 64
data_directory = os.path.join(STORAGE_PATH, 'orig')
here_live_model_versions = os.path.join(STORAGE_PATH, 'models')
model_classes_loc = os.path.join(STORAGE_PATH, 'models/temathic')


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


def predict_m(umid, dataset):
    old_model = f'{here_live_model_versions}/{choose_last_version(here_live_model_versions)}/model'
    test_set = get_predict_dataloader(dataset, our_transform_pipeleine)
    modelka = torch.load(old_model)
    predict_generator = modelka.predict(test_set)
    results =[]
    for i in  predict_generator:
        img = os.path.split(i['predict_generator'])[1]
        classlabels = i['features']
        result.append({'id': img, 'labels': classlabels})

    update_progress_done(json.dumps(result))


def retrain(umid, class_name):
    interesting_zone = [class_name]
    train_loaders, val_loaders = get_loaders(data_directory, our_transform_pipeleine, inter_area = interesting_zone)
    train_int_mod(interesting_zone, train_loaders, val_loaders)
    
    old_model = f'{here_live_model_versions}/{choose_last_version(here_live_model_versions)}/model'
    old_classes = f'{here_live_model_versions}/{choose_last_version(here_live_model_versions)}/class_labels.json'

    new_wersion = int(choose_last_version(here_live_model_versions)[2:]) + 1
    new_mod = f'{here_live_model_versions}/id{new_wersion}/model'
    new_cls = f'{here_live_model_versions}/id{new_wersion}/class_labels.json'
    p = subprocess.Popen(f'mkdir {here_live_model_versions}/id{new_wersion}', shell = True, stderr=subprocess.PIPE, stdin = subprocess.PIPE)
    out, err = p.communicate()

    modelka = TransportPredictionscrambled(interesting_zona = interesting_zone, model_int = old_model, model_classes = old_classes)
    modelka.save_model(new_mod, json_path = new_cls)
    update_progress_done(json.dumps({'umid': 'm666'}))
