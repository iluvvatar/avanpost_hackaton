import os
import math
import copy
import warnings
import json
import subprocess

import pandas as pd
import numpy as np

import torch
import torchvision

from skimage.io import imread

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class ImageStorage:
    ROOT = "/home/ilyaroot/storage/data"
