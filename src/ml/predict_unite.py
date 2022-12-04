
import os
import math
import copy
import warnings
import json
import subprocess

import torch
import torchvision

from skimage.io import imread
from torchvision.io import read_image

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from copy import deepcopy


model = torchvision.models.quantization.resnet50(weights = True)

our_transform_pipeleine  = (
    torchvision.transforms.ToPILImage(mode = 'RGB'),
    torchvision.transforms.Resize(size=(224, 224)),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    )


class TransportDataToPredict(torch.utils.data.Dataset):
  def __init__(self, dataset_path, transform = None):
    self.dataset_path = dataset_path
    self.transform = transform
  def __getitem__(self, img_loc):
    cl = os.path.split(img_loc)[0]
    img_path = os.path.join(self.dataset_path, img_loc)
    img = read_image(img_path)
    if self.transform:
      try:
         img = self.transform(img)
      except:
         return None
    sample = {'value': img,
              'path': img_loc}
    return sample



def get_predict_dataloader(folder, our_transform_pipeleine):
    make_img_transform = torchvision.transforms.Compose(
        our_transform_pipeleine
    )
    
    data_transporter = TransportDataToPredict(dataset_path=data_directory,
        transform=make_img_transform)

    transporter = torch.utils.data.DataLoader(
        data_transporter,
        batch_size=batch_size,
        sampler=torch.utils.data.SubsetRandomSampler([f'{folder}/{i}' for i in os.listdir(folder)]))
    return transporter


def scramble(interesting_zone = None, model = None, model_classes = None):
    fcs = []
    max_class = -1

    if model_classes:
        with open(model_classes, 'r') as file:
            try:
                classes = json.load(file)
            except:
                classes = {}
            else: 
                classes = classes
                max_class = max(classes.values())

    if model:         
        int_modelka = torch.load(model)
        for i in int_modelka.fc:
            fcs.append(i)

    if interesting_zone:
        for i in interesting_zone:
            classes[i] = max_class + 1
            int_modelka = torch.load(f'{model_classes_loc}/{i}.model')
            fcs.append(int_modelka.fc)
            max_class += 1
    return fcs, classes



class TransportPredictionscrambled(torch.nn.Module):
    def __init__(self, interesting_zona = None, model_int = None, model_classes = None, model = model):
        super(TransportPredictionscrambled, self).__init__()
        fc, clas_dics = scramble(interesting_zone = interesting_zona, model = model_int, model_classes = model_classes)
        self.conv1 = model.conv1
        self.bn1 = model.bn1
        self.relu = model.relu
        self.maxpool = model.maxpool
        self.layer1 = model.layer1
        self.layer2 = model.layer2
        self.layer3 = model.layer3
        self.layer4 = model.layer4
        self.avgpool = model.avgpool
        self.fc = torch.nn.ModuleList(fc)
        self.requires_grad = False
        self.clas_dics = clas_dics

    def save_model(self, path, json_path = None):
        torch.save(self, path)
        if json_path:
            with open(json_path, 'w') as out_json:
                json.dump(self.clas_dics, out_json)
        return 'Model saved sucessefully'

    def forward(self, y):
        y = self.conv1(y)
        y = self.bn1(y)
        y = self.relu(y)
        y = self.maxpool(y)
        y = self.layer1(y)
        y = self.layer2(y)
        y = self.layer3(y)
        y = self.layer4(y)
        y = self.avgpool(y)
        y = torch.flatten(y, 1)
        y = torch.column_stack([layer(y) for layer in self.fc])
        return y    

    def predict(self, data_loader):
        cdr = {self.clas_dics[i]: i for i in self.clas_dics.keys()} 
        if USE_GPU:
            self.cuda()
        lables_all = []
        predicts_all = []
        paths_all = []
        for j, batch in enumerate(data_loader):
            X = batch['value']
            paths = batch['path']
            if USE_GPU:
                X = X.cuda()
            with torch.set_grad_enabled(False): 
                y = self(X)
            paths_all += paths
            for pred, path in zip (y, paths):
                clar = []
                for cl in cdr.keys():
                    if pred[2*cl + 1]/(pred[2*cl]+pred[2*cl + 1]) > 0.55:
                        clar.append(cdr[cl])
                yield {'path': path, 'features': clar}

#old_model = f'{here_live_model_versions}/{choose_last_version(here_live_model_versions)}/model#old_classes = f'{here_live_model_versions}/{choose_last_version(here_live_model_versions)}/class_labels.json'

#new_wersion = int(choose_last_version(here_live_model_versions)[2:]) + 1
#new_mod = f'{here_live_model_versions}/id{new_wersion}/model'
#new_cls = f'{here_live_model_versions}/id{new_wersion}/class_labels.json'
#p = subprocess.Popen(f'mkdir {here_live_model_versions}/id{new_wersion}', shell = True, stderr=subprocess.PIPE, stdin = subprocess.PIPE)
#out, err = p.communicate()

#modelka = TransportPredictionscrambled(interesting_zona = interesting_zone, model_int = old_model, model_classes = old_classes)
#modelka.save_model(new_mod, json_path = new_cls)


#old_model = f'{here_live_model_versions}/{choose_last_version(here_live_model_versions)}/model'
#test_set = get_predict_dataloader('/home/egorml/test_ds', our_transform_pipeleine)
#modelka = torch.load(old_model)
#q = modelka.predict(test_set)
#print(q)
#for i in q: 
 #   print(i)
