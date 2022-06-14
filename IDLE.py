# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

import random
import os
from utils.file_reader import YamlReader
import yaml
from Syrius_API.flagship.res_notify import send_order
from utils.log import logger
from time import sleep
import itertools
from base.common import *

ll = '122111221'