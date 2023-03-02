import os

import yaml


class util():

    def get_project_path(self, project_name=None):
        """
        获取当前项目根路径
        :param project_name:当前项目的名称
        :return: 根路径
        """
        PROJECT_NAME = 'SSH' if project_name is None else project_name
        project_path = os.path.abspath(os.path.dirname(__file__))
        root_path = project_path[:project_path.find("{0}{1}".format(PROJECT_NAME, os.path.sep)) +
                                  len("{0}{1}".format(PROJECT_NAME, os.path.sep))]
        # print('当前项目名称：{}\r\n当前项目根路径：{}'.format(PROJECT_NAME, root_path))
        return root_path

    def read_yaml(self, path):
        """
        读取yaml文件
        :param path:
        :return:
        """
        with open(rf"{self.get_project_path()}{os.path.sep}{path}", mode='r', encoding='utf-8') as file:
            msg = yaml.safe_load(file)
        return msg


if __name__ == '__main__':
    print(util().read_yaml(f'resources{os.path.sep}robot_wifi.yaml'))
