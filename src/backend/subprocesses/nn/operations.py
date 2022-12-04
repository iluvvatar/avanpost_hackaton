import os
import json

from ml.ml_megascript import *
from backend.subprocesses.events import update_progress, update_progress_done

a = TransportPredictionscrambled

STORAGE_PATH = os.getenv('STORAGE_PATH', '/storage/data')
ORIG_STORAGE_PATH = os.path.join(STORAGE_PATH, 'orig')

MAX_EPOCHS = 150
USE_GPU = True
ESR = 5
batch_size = 64
data_directory = '/storage/data/orig'
here_live_model_versions = '/storage/data/models'
model_classes_loc = '/storage/data/models/temathic'

def predict_single(muid, filename):
    update_progress_done(
            json.dumps({'label': 'snowboard', 'probability': 1.0}))


def predict(umid, dataset):
    old_model = f'{here_live_model_versions}/{choose_last_version(here_live_model_versions)}/model'
    test_set = get_predict_dataloader(dataset, our_transform_pipeleine)
    modelka = TransportPredictionscrambled()
    modelka = torch.load(old_model)
    predict_generator = modelka.predict(test_set)
    for i in  predict_generator:
        img = os.path.split(i['predict_generator'])[1]
        classlabels = i['features']
    update_progress_done(json.dumps({'snowboard': {'precision': 0.9, 'recall': 0.6}}))

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
