# -*- coding: gbk -*-

import os
import datetime


def create_output_dir():
    """�������Ŀ¼"""
    output_dir = "reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir
