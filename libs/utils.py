# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2022-12-19 10:53:56
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-03 14:07:59
@FilePath: /labelp/libs/utils.py
@Description:
'''
import math
import os
from collections import defaultdict

import numpy as np

from PyQt5.QtGui import QImage

def get_sample_file(dir_path, filter=('.jpg', )):
    data_list = defaultdict(dict)
    for item in os.listdir(dir_path):
        item = os.path.join(dir_path, item)
        if os.path.isdir(item):
            one_dir_sample = {
                't': None,
                's': [],
            }
            for file in os.listdir(item):
                file = os.path.join(item, file)
                if os.path.isfile(file):
                    file_path, ext = os.path.splitext(file)
                    if ext in filter:
                        if file_path.endswith("_t"):
                            one_dir_sample['t'] = file
                        else:
                            one_dir_sample['s'].append(file)
            if one_dir_sample['t'] and one_dir_sample['s']:
                data_list[item] = one_dir_sample

    return data_list

def distance(p):
    return math.sqrt(p.x() * p.x() + p.y() * p.y())

def distancetoline(point, line):
    p1, p2 = line
    p1 = np.array([p1.x(), p1.y()])
    p2 = np.array([p2.x(), p2.y()])
    p3 = np.array([point.x(), point.y()])
    if np.dot((p3 - p1), (p2 - p1)) < 0:
        return np.linalg.norm(p3 - p1)
    if np.dot((p3 - p2), (p1 - p2)) < 0:
        return np.linalg.norm(p3 - p2)
    if np.linalg.norm(p2 - p1) == 0:
        return 0
    return np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)

def toQImage(file_path):
    ext=os.path.splitext(file_path)[-1]
    if ext in (".csv",".CSV"):
        pass
        img=None
    else:
        with open(file_path, 'rb') as f:
            img=QImage.fromData(f.read())

    return img

