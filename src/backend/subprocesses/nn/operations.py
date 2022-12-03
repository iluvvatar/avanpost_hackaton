import json


from backend.subprocesses.events import update_progress, update_progress_done


def predict_single(muid, filename):
    update_progress_done(
            json.dumps({'label': 'snowboard', 'probability': 1.0}))


def predict():
    pass


def retrain():
    pass
