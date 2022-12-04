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