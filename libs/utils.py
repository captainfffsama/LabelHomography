# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2022-12-19 10:53:56
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-01-11 15:44:49
@FilePath: /label_homography/libs/utils.py
@Description:
'''
import math
import os
from collections import defaultdict

import numpy as np
import cv2

from PyQt5.QtGui import QImage, QTransform
from PyQt5.QtCore import QPoint, QPointF, Qt


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
    ext = os.path.splitext(file_path)[-1]
    if ext in (".csv", ".CSV"):
        pass
        img = None
    else:
        with open(file_path, 'rb') as f:
            img = QImage.fromData(f.read())

    return img


def countH(ps1, ps2):
    ps1 = np.array(ps1)
    ps2 = np.array(ps2)
    H, Mask = cv2.findHomography(ps1, ps2, cv2.RANSAC, 5, maxIters=100)

    return H, Mask


def QPointF2QPoint(p: QPointF):
    return QPoint(int(p.x()), int(p.y()))


def QImage2Mat(incomingImage: QImage) -> np.ndarray:
    '''  Converts a QImage into an opencv MAT format  '''

    incomingImage = incomingImage.convertToFormat(4)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr


def Mat2QImage(img: np.ndarray) -> QImage:
    img = np.transpose(img, (1, 0, 2)).copy()
    return QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)


def ndarray2QTransform(nparray: np.ndarray) -> QTransform:
    vs = nparray.flatten().tolist()
    return QTransform(*vs)


def printQTransform(transform: QTransform):
    print("[[{},{},{}], \n[{},{},{}], \n[{},{},{}]]\n".format(
        transform.m11(), transform.m12(), transform.m13(), transform.m21(),
        transform.m22(), transform.m23(), transform.m31(), transform.m32(),
        transform.m33()))


def generateHomographyImage(img1: QImage, img2: QImage,
                            H: np.ndarray) -> QImage:
    img1 = Mat2QImage(img1)
    img2 = Mat2QImage(img2)


def convertpt2matrix(pts):
    if isinstance(pts, list):
        pts = np.array([x + [1] for x in pts])
    if pts.shape[-1] == 2:
        expend_m = np.array([[1], [1], [1], [1]])
        pts = np.concatenate((pts, expend_m), axis=1)
    return pts


def generate_transform_pic(imgb_shape, imgA, H):
    imgA_warp = cv2.warpPerspective(imgA,
                                    H,
                                    imgb_shape,
                                    flags=cv2.INTER_LINEAR)

    k_pts = [[0, 0], [0, imgA.shape[0] - 1],
             [imgA.shape[1] - 1, imgA.shape[0] - 1], [imgA.shape[1] - 1, 0]]

    kptm = convertpt2matrix(k_pts)
    warp_kpm = np.matmul(H, kptm.T)
    warp_kpm = (warp_kpm / warp_kpm[2, :])[:2, :].astype(int).T.reshape(
        (-1, 1, 2))
    breakpoint()
    # FIXME:这里可能有问题,没做越界
    # cv2.polylines(imgA_warp,[warp_kpm],True,(0,0,255),thickness=5)
    return imgA_warp