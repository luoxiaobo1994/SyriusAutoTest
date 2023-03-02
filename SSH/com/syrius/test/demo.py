import re


def test():
    if True and False:
        print('1')
    elif True and True:
        print('2')

def test1():
    checker_map = {
        'handle_robotic_amixer_settings.service': 'enabled',
        'handle_robotic_can_bus_enable.service': 'enabled',
        'buzzard_ota.service': 'enabled',
        'buzzard_permission_define.service': 'enabled',
        'syrius-boot-sound.service': 'enabled',
        'syrius-net-player.service': 'enabled',
        'syrius-psyche.service': 'enabled'
    }
    for key, values in checker_map.items():
        print(f"key:{key},value:{values}")


def change_num(param):
    """
    用户权限字符串转化为数字
    :param param:
    :return:
    """
    param = param[1:]
    paramArray = re.findall(r'.{3}', param)
    param_value = ''
    for one_param in paramArray:
        if one_param == '--x':
            param_value += '1'
        elif one_param == '-w-':
            param_value += '2'
        elif one_param == 'r--':
            param_value += '4'
        elif one_param == '-wx':
            param_value += '3'
        elif one_param == 'r-x':
            param_value += '5'
        elif one_param == 'rw-':
            param_value += '6'
        elif one_param == 'rwx':
            param_value += '7'
    return param_value


if __name__ == '__main__':
    test()

# temp = 'secbot   secbot   java -XX:+UseSerialGC -verbose:gc -Xss512k -Xmx20m -Xmn8m -XX:MaxDirectMemorySize=8m -DLOG_HOME=/var/log/cosmos/secbot -jar secbot-1.0-c485.jar'
# temp= re.split('[ ]{3,4}', temp)
# print(temp)
