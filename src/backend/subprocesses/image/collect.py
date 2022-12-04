import os
import json
from serpapi import GoogleSearch
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.
from googleapiclient.http import MediaIoBaseDownload
from operator import itemgetter
import io
import requests
import shutil
import uuid
import time  # DEBUG
from backend.subprocesses.events import update_progress, update_progress_done

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MOCKED_DATA_PATH = os.path.join(os.getenv('STORAGE_PATH'),
                                'mocked_image_search_response.json')
DRIVE_PATH = os.getenv('DRIVE_PATH')
TOKEN = os.path.join(DRIVE_PATH, 'token.json')
CREDENTIALS = os.path.join(DRIVE_PATH, 'credentials.json')

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file'
          ]


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


def get_from_drive(path, file_id):
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('drive', 'v3', credentials=creds)
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False: # blocking
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
    except HttpError as error:
        print(f'An error occurred: {error}')


def get_dataset(path, link):
    # https://drive.google.com/file/d/1VanGBXY1FdcTR1XPJP96Y3ATuZxDWHcY/view?usp=share_link
    file_id = link.split('/')[5] # 5 position of file_id
    path = os.path.join(path, f'{file_id}.tar')
    get_from_drive(path, file_id)

