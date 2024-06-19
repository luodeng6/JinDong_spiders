"""
    公共函数
    :time: 2024/05/15
    :version: 1.0.0
    :author: 罗邓
"""
import json
import os
from xml import etree
from lxml.etree import Element


def saveJson(data, filename) -> bool:
    """
        保存字典数据到json文件
        :param data: 要保存的数据
        :param filename: 保存的文件名
        :return: bool
        :time: 2024/05/15
        :author: 罗邓
     """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            print(f"{filename}，数据保存成功^v^")
            return True
    except Exception as e:
        print(f"{filename}，数据保存失败^~^")
        return False


def getElementText(element: Element) -> str:
    """
        获取element元素的文本内容--->整个元素的文本内容
        :param element: 要获取文本内容的元素
        :return: str
        :time: 2024/05/15
        :author: 罗邓

        getElementText: 获取给定元素 element 内部的文本内容
        使用XPath来选择该元素内部的所有文本节点，
        并将它们连接成一个字符串，并去除两端的空白字符后返回
     """
    return ''.join(element.xpath('.//text()')).strip()


def openElement(element: Element) -> str:
    """
        展开element元素的方法,形式为字符串: 将XML元素转换为字符串
        :param element: 要展开的元素
        :return: str
        :time: 2024/05/15
        :author: 罗邓
     """
    return etree.tostring(element, encoding='unicode')


def read_folder_data(folder_path: str) -> list:
    """
    读取文件夹下所有文件->返回文件路径，供后续处理
    :param folder_path: 文件夹路径
    :return: 文件夹下所有文件   list
    :time: 2024/05/15
    :author: 罗邓
    """
    data_list = []  # 存储所有文件的数据->list ，每个元素为文件路径
    # 遍历文件夹下所有文件
    for file_name in os.listdir(folder_path):
        # 拼接路径
        file_path = os.path.join(folder_path, file_name)
        # 判断是否为文件->是文件才读取
        if os.path.isfile(file_path):
            data_list.append(file_path)
    return data_list


def save_merge_data(data_list: list, filename: str) -> bool:
    """
    保存合并后的数据
    :param data_list: 合并后的数据
    :param filename: 保存的文件名
    :return: 保存成功返回True，失败返回False
    :time: 2024/05/15
    :author: 罗邓
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # 保存数据->数据列表写入到JSON文件
            json.dump(data_list, f, ensure_ascii=False)
            print(f"{filename}，数据保存成功^v^")
            return True
    except Exception as e:
        print(f"{filename}，数据保存失败^~^")
        return False


# 数据转换函数
def convert_to_integer(input_string):
    if "+" in input_string:
        input_string = input_string.replace("+", "")
        if "万" in input_string:
            return int(float(input_string.replace("万", "")) * 10000)
        else:
            return int(input_string)
    else:
        if "万" in input_string:
            return int(float(input_string.replace("万", "")) * 10000)
        else:
            return int(input_string)


def 遍历文件夹的所有文件_然后一个一个重命名文件():
    folder_path = '../data/'
    index = 1
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)  # 构建完整的文件路径

        # 检查是否为文件
        if os.path.isfile(file_path):
            # 新的文件名（这里以在原文件名前加上"new_"作为示例）
            new_filename = f'第{index}页data.json'
            # 构建新的完整文件路径
            new_file_path = os.path.join(folder_path, new_filename)
            # 重命名文件
            os.rename(file_path, new_file_path)
            index += 1


def 统计所有文件的数据量():
    # 遍历文件夹下所有json文件->读取为一个一个字典数据格式
    folder_path = '../data/'
    tatol_num = 0

    for filename in os.listdir(folder_path):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)

        # 文件是否为JSON文件
        if filename.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                # 读取JSON文件内容并转换为字典
                data = json.load(file)
                # 统计数据量
                tatol_num += data['len']
    print(f"数据总量:{tatol_num}")


# 获取评论接口地址->根据当前页码和产品ID动态生成评论接口地址
def getPingLunUrl(current_page, productId):
    return f"https://color.jd.hk/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&t=1715775567350&loginType=3&uuid=181809404.17157048140831793190534.1715704814.1715772395.1715775471.3&productId={productId}&score=0&sortType=5&page={current_page}&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield="
