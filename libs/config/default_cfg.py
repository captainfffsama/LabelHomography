# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2022-12-19 10:42:01
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2022-12-19 10:45:32
@FilePath: /labelp/libs/config/default_cfg.py
@Description:
'''
import json

param = dict(
    default_dir="./",
)


def _update(dic1: dict, dic2: dict):
    """使用dic2 来递归更新 dic1
        # NOTE:
        1. dic1 本体是会被更改的!!!
        2. python 本身没有做尾递归优化的,dict深度超大时候可能爆栈
    """
    for k, v in dic2.items():
        if k.endswith('args') and v is None:
            dic2[k] = {}
        if k in dic1:
            if isinstance(v, dict) and isinstance(dic1[k], dict):
                _update(dic1[k], dic2[k])
            else:
                dic1[k] = dic2[k]
        else:
            dic1[k] = dic2[k]

def _merge_json(json_path: str):
    global param
    with open(json_path, 'r') as fr:
        content_dict = json.load(fr)
    _update(param, content_dict)


def merge_param(file_path: str):
    """按照用户传入的配置文件更新基本设置
    """
    cfg_ext = file_path.split('.')[-1]
    func_name = '_merge_' + cfg_ext
    if func_name not in globals():
        raise ValueError('{} is not support'.format(cfg_ext))
    else:
        globals()[func_name](file_path)
