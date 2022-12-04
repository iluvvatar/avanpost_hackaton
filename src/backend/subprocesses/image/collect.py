import os
import json
from serpapi import GoogleSearch
from operator import itemgetter
import requests
import shutil
import uuid
import time  # DEBUG


from backend.subprocesses.events import update_progress, update_progress_done

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MOCKED_DATA_PATH = os.path.join(os.getenv('STORAGE_PATH'),
                                'mocked_image_search_response.json')


def mocked(search):
    def const(*args, **kwargs):
        with open(MOCKED_DATA_PATH, 'r') as f_in:
            return map(itemgetter('thumbnail'), json.load(f_in))
    return const


@mocked
def make_google_search(query, page=0):
    params = {
        'q': query,
        'tbm': 'isch',
        'ijn': str(page),
        'api_key': GOOGLE_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return map(itemgetter('thumbnail'), results)


def get_images_from_google(path, class_name, num_doc=10, drawn_ratio=0.0):
    path = os.path.join(path, class_name)
    if not os.path.exists(path):
        os.mkdir(path)

    page, downloaded = 0, 0
    for page in range(10):
        links = make_google_search(class_name, page)
        for link in links:
            time.sleep(2)
            response = requests.get(link, stream=True)
            if response.status_code == 200:
                filename = os.path.join(path, str(uuid.uuid4()))
                with open(filename, 'wb') as f_out:
                    response.raw_decode_content = True
                    shutil.copyfileobj(response.raw, f_out)
                    downloaded += 1
                    update_progress(100.0 * downloaded / num_doc)
                    if downloaded >= num_doc:
                        res = {'num_doc': num_doc, 'downloaded': downloaded}
                        update_progress_done(json.dumps(res))
                        return

    res = {'num_doc': num_doc, 'downloaded': downloaded}
    update_progress_done(json.dumps(res))
    update_progress_done(f'{num_doc} > {downloaded}')

    # drawn_num_doc = int(drawn_ratio * num_doc)
    # TODO: make_google_search(f'drawn {class_name}')


def get_image(path, link):
    time.sleep(2)
    response = requests.get(link, stream=True)
    if response.status_code == 200:
        filename = os.path.join(path, str(uuid.uuid4()))
        with open(filename, 'wb') as f_out:
            response.raw_decode_content = True
            shutil.copyfileobj(response.raw, f_out)
    update_progress_done(json.dumps({'filename': filename}))


def get_dataset(path, link):
    for i in range(100):
        time.sleep(2)
        update_progress(i)

    update_progress_done(json.dumps({'path': '...'}))
