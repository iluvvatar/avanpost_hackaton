import json


from backend.subprocesses.events import update_progress, update_progress_done


def predict_single(muid, filename):
    update_progress_done(
            json.dumps({'label': 'snowboard', 'probability': 1.0}))


def predict(umid, dataset):
    update_progress_done(json.dumps({'snowboard': {'precision': 0.9, 'recall': 0.6}}))


def retrain(umid, class_name):
    update_progress_done(json.dumps({'umid': 'm666'}))
