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


MAX_EPOCHS = 150
USE_GPU = True
ESR = 5
batch_size = 64
data_directory = '/storage/data/orig'
here_live_model_versions = '/storage/data/models'
model_classes_loc = '/storage/data/models/temathic'


def choose_last_version(here_live_model_versions):
    lmv = 0
    for i in os.listdir(here_live_model_versions):
        if i.startswith('id'):
            v = int(i[2:])
            if v > lmv:
                lmv = v
    return f'id{lmv}'


def get_last_classes(last_model_params):
    with open(last_model_params, 'r') as file:
        try:
            classdict = json.load(file)
        except:
            classdict = {}
        else: 
            classdict = classdict
    return classdict

def choose_area_of_interest(data_directory, here_live_model_versions):
    lmv = choose_last_version(here_live_model_versions)
    classdict = get_last_classes(f'{here_live_model_versions}/{lmv}/class_labels.json')
    for i in os.listdir(data_directory):
        if i not in classdict.keys():
            if i != 'unknown':
                yield i

model = torchvision.models.quantization.resnet50(weights = True)

class TransportData(torch.utils.data.Dataset):
  def __init__(self, dataset_path, my_dset, transform = None):
    self.dataset_path = dataset_path
    self.transform = transform
    self.my_dset = my_dset
  def __getitem__(self, img_loc):
    cl = os.path.split(img_loc)[0]
    img_path = os.path.join(self.dataset_path, img_loc)
    img = read_image(img_path)
    if self.transform:
      try:
         img = self.transform(img)
      except:
         return None
    cl = 1 if img_loc.startswith(self.my_dset) else 0
    sample = {'label': cl,
              'value': img,
              'path': img_loc}
    return sample


def get_dset_names(dataset_path):
    class_dict = {}
    for class_name in os.listdir(dataset_path):
        dirpa = os.path.join(dataset_path, class_name)
        class_dict[class_name] = []
        imgs = [os.path.join(class_name, i) for i in os.listdir(dirpa)]
        imcorr = []
        for i in imgs:
            try:
                im = imread(f'{data_directory}/{i}')
                torchvision.transforms.ToPILImage(mode = 'RGB')(im)
            except:
                pass
            else:
                imcorr.append(i)
        class_dict[class_name] = imcorr
    return class_dict

def get_sets_to_model(class_dict, inter_area = None):
    dsets_val = {}
    dsets_train = {}
    for i in class_dict.keys():
        if inter_area and i not in inter_area:
            continue
        my_50_train, my_50_val = train_test_split(class_dict[i], test_size = 0.2)
        l_tr = len(my_50_train)
        l_val = len(my_50_val)
        for j in class_dict.keys():
            if j!=i:
                his_50_train, his_50_val = train_test_split(class_dict[j], test_size = 0.2)
                his_50_train, his_50_val = his_50_train[:int(l_tr/(len(class_dict) - 1))], his_50_val[:int(l_val/(len(class_dict) - 1))]
                my_50_train += his_50_train
                my_50_val += his_50_val
        dsets_train[i] = my_50_train
        dsets_val[i] = my_50_train
    return dsets_train, dsets_val

def get_ds(dataset_path, inter_area = None):
    class_dict = get_dset_names(dataset_path)
    dsets_train, dsets_val = get_sets_to_model(class_dict, inter_area = inter_area)
    return dsets_train, dsets_val


our_transform_pipeleine  = (
    torchvision.transforms.ToPILImage(mode = 'RGB'),
    torchvision.transforms.Resize(size=(224, 224)),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    )

def get_loaders(data_directory, our_transform_pipeleine, batch_size = 64, inter_area = None):

    train_d, val_d = get_ds(data_directory, inter_area = inter_area)
  
    make_img_transform = torchvision.transforms.Compose(
        our_transform_pipeleine
    )
    
    data_transporter = lambda x: TransportData(
        dataset_path=data_directory,
        my_dset=x,
        transform=make_img_transform,)
    
    train_loaders = {
        i: torch.utils.data.DataLoader(
          data_transporter(i),
          batch_size=batch_size,
          sampler=torch.utils.data.SubsetRandomSampler(train_d[i]))
          for i in train_d.keys()}
    val_loaders = {
        i: torch.utils.data.DataLoader(
          data_transporter(i),
          batch_size=batch_size,
          sampler=torch.utils.data.SubsetRandomSampler(val_d[i]))
          for i in val_d.keys()}
    return train_loaders, val_loaders

class TransportPrediction(torch.nn.Module):
    def __init__(self, model):
        super(TransportPrediction, self).__init__()
        self.conv1 = model.conv1
        self.bn1 = model.bn1
        self.relu = model.relu
        self.maxpool = model.maxpool
        self.layer1 = model.layer1
        self.layer2 = model.layer2
        self.layer3 = model.layer3
        self.layer4 = model.layer4
        self.avgpool = model.avgpool
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(in_features=2048, out_features=2, bias=True),
            torch.nn.Sigmoid())
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
    
    def save_model(self, path):
        torch.save(self, path)
        return 'Model saved sucessefully'
    
    def fit(self, train_dl, val_dl, max_epochs = MAX_EPOCHS, early_stopping_rounds = ESR, model_path = None):
        accs = []
        losses = []
        self.fc.requires_grad = True
        if USE_GPU:
            self = self.cuda()
        optimizer = torch.optim.Adam(model.parameters())
        loss_function = torch.nn.BCELoss()
        best_acc = 0.0
        best_round = 0
        local_best_round = 0
        local_best_acc = 0.0
        for epo in range(MAX_EPOCHS):
            samples = 0
            loss_sum = 0
            correct_sum = 0
            for phase in ["train", "val"]:
                if phase == "train":
                    self.train()
                else: 
                    self.eval()
                dl = train_dl if phase == 'train' else val_dl
                for j, batch in enumerate(dl):
                    if j%50 == 49: 
                        print(f'Counting {j+1} batch')
                    X = batch["value"]
                    labels = batch["label"]
                    if USE_GPU:
                        X = X.cuda()
                        labels = labels.cuda()
                    labels = torch.nn.functional.one_hot(labels, 2).to(torch.float32)
                    optimizer.zero_grad()
                    with torch.set_grad_enabled(phase == 'train'):
                        y = self(X)
                        loss = loss_function(y, labels)
                        if phase == "train":
                            loss.backward()
                            optimizer.step()
                            loss_sum += loss.item() * X.shape[0]
                            samples += X.shape[0]
                        else:
                            ans_classes = (y[:, 1] > 0.5).type(torch.float32)
                            num_corrects = int((ans_classes == labels).sum()) 
                            correct_sum += num_corrects
            epoch_acc, epoch_loss = 0, 0
            if float(samples):
                epoch_acc = float(correct_sum) / float(samples)
                epoch_loss = float(loss_sum) / float(samples)
                accs.append(epoch_acc)
                losses.append(epoch_loss)
                print(f'Epoch no. {epo} Accuracy: {epoch_acc} Loss {epoch_loss} Prgress {int(epo/max_epochs) * 100}%')
            
            if phase == "val" and epoch_acc > best_acc:
                best_acc = epoch_acc
                if model_path:
                    torch.save(self, model_path)
            if phase == "val" and epoch_acc <= local_best_acc:
                local_best_round += 1
                if local_best_round >= early_stopping_rounds:
                    self.requires_grad = False
                    return {'accuracy': accs,
                    'loss': losses,
                    'best_accuracy': best_acc,
                    'best_model_wts': best_model_wts,
                    'early_stopping': True,
                    'epochs': epo}
            if phase == "val" and epoch_acc > local_best_acc:
                local_best_round = 0
                local_best_acc = epoch_acc
        self.requires_grad = False
        return {'accuracy': accs,
        'loss': losses,
        'best_accuracy': best_acc,
        'early_stopping': False,
        'epochs': epo}


def train_int_mod(interesting_zone, train_loaders, val_loaders):
    for i in interesting_zone:
        if os.isfile(f'{model_classes_loc}/{i}.model'):
            continue
        intmod = TransportPrediction(model)
        pars_int = intmod.fit(train_loaders[i], val_loaders[i])
        intmod.save(f'{model_classes_loc}/{i}.model')
        with open(f'{model_classes_loc}/{i}.model.json', 'w') as file:
            json.dump(pars_int, file)
    return



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
            if i not in classes.keys():
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

