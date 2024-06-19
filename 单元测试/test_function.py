import json
import os

from public import read_folder_data

"""
 单元测试
"""


def one_test():
    folder_path = '/data'
    data_list = []  # 存储所有文件的数据
    # 遍历文件夹下所有文件
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            print(file_path)
            data_list.append(file_path)

    print(data_list)


def two_test():
    if {}:
        print("非空字典")
    else:
        print("空字典")


if __name__ == '__main__':
    two_test()
