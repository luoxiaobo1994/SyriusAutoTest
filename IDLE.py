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


os.system(
                    f'adb -s 10.2.10.229:5555 shell am start -n "com.syriusrobotics.platform.launcher/com.syriusrobotics.platform.jarvis.'
                    f'SplashActivity" -a android.intent.action.MAIN -c android.intent.category.LAUNCHER')
