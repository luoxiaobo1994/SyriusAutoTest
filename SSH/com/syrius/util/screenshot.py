import datetime
import os
from com.syrius.util.commonUtil import util

#
# def get_project_path(project_name=None):
#     """
#     获取当前项目根路径
#     :param project_name:当前项目的名称
#     :return: 根路径
#     """
#     PROJECT_NAME = 'SSH' if project_name is None else project_name
#     project_path = os.path.abspath(os.path.dirname(__file__))
#     root_path = project_path[:project_path.find("{}\\".format(PROJECT_NAME)) + len("{}\\".format(PROJECT_NAME))]
#     # print('当前项目名称：{}\r\n当前项目根路径：{}'.format(PROJECT_NAME, root_path))
#     return root_path



def screenshot():
    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")[:-3]
    fileDir = file_name[:file_name.find("_")]
    # print(fileDir)
    file_path = f"{util().get_project_path()}/file/picture/{fileDir}"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # 执行截图指令
    os.system(f"adb exec-out screencap -p > {file_path}/{file_name}.png")


    print(f"成功打印出文件【{file_name}.png】")

if __name__ == '__main__':
    screenshot()
    # print(get_project_path())
