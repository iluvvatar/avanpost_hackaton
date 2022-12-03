import os
import json
from serpapi import GoogleSearch
from operator import itemgetter
import requests
import shutil
import uuid
from events import update_progress, update_progress_done
import time  # DEBUG

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MOCKED_DATA_PATH = 'data/mocked_image_search_response.json'


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
    page, downloaded = 0, 0
    for page in range(10):
        links = make_google_search(class_name, page)
        for link in links:
            time.sleep(2)
            response = requests.get(link, stream=True)
            if response.status_code == 200:
                filepath = os.path.join(path, str(uuid.uuid4()))
                with open(filepath, 'wb') as f_out:
                    response.raw_decode_content = True
                    shutil.copyfileobj(response.raw, f_out)
                    downloaded += 1
                    update_progress(100.0 * downloaded / num_doc)
                    if downloaded >= num_doc:
                        update_progress_done('...')
                        return

    # drawn_num_doc = int(drawn_ratio * num_doc)
    # TODO: make_google_search(f'drawn {class_name}')
