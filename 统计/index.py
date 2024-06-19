"""
    @name: index.py
    @file: index.py
    @author: 罗邓
    @date: 2023/10/13
    @desc: 汇总各所有数据到JSON
    @version: 1.0
"""
import json
import os
import pandas as pd
from pandas import DataFrame
from public import read_folder_data, saveJson, convert_to_integer, 遍历文件夹的所有文件_然后一个一个重命名文件, \
    统计所有文件的数据量


def Statistics_all_To_JSON():
    """
    @name: Statistics_all_To_JSON
    统计所有爬取的JSON数据（在data目录下）并整合到JSON
    :return: JSON
    :rtype: dict
    """
    # 读取爬取 文件夹中的所有JSON文件 获取所有文件路径
    file_list = read_folder_data("../data/")
    # 整合数据到JSON
    data_list = []
    # 遍历所有文件
    for file_name in file_list:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data['data']:
                data_list.append(item)
    data_Json = {'data': data_list, 'len': len(data_list)}
    # 获取到包含所有数据的字典
    return data_Json


# 获取包含所有数据的 字典格式化为需要的格式 并转换为DataFrame 
def Statistics_all_To_DataFrame() -> DataFrame:
    data_Json = Statistics_all_To_JSON()
    # 从JSON获取到包含所有数据的列表
    data_list = data_Json['data']
    data_Excel = []

    for data in data_list:
        data_item = {}
        data_item['title'] = data['title']
        data_item['ShopName'] = data['ShopName']
        data_item['DetailsUrl'] = data['DetailsUrl']
        data_item['imgUrl'] = data['imgUrl']
        data_item['price'] = data['price']

        data_item["好评数"] = data['统计信息']['好评数']
        data_item["好评率"] = data['统计信息']['好评率'].replace('%', '')
        data_item["差评"] = data['统计信息']['差评']
        data_item["追评数"] = data['统计信息']['追评数']
        data_item["总评论数"] = data['统计信息']['总评论数']

        data_item["品牌信息"] = data['统计信息']['商品信息'].get('品牌信息', "空")
        data_item["商品名称"] = data['统计信息']['商品信息'].get('商品名称', "空")
        data_item["商品编号"] = data['统计信息']['商品信息'].get('商品编号', "空")
        data_item["类别"] = data['统计信息']['商品信息'].get('类别', "空")
        data_item["药品剂型"] = data['统计信息']['商品信息'].get('药品剂型', "空")
        data_item["适用人群"] = data['统计信息']['商品信息'].get('适用人群', "空")
        data_item["使用方法"] = data['统计信息']['商品信息'].get('使用方法', "空")
        data_item["国产/进口"] = data['统计信息']['商品信息'].get('国产/进口', "空")

        """
          "品牌信息": "舒尔佳",
          "商品名称": "舒尔佳奥利司他胶囊",
          "商品编号": "100011335310",
          "类别": "西药",
          "药品剂型": "胶囊剂",
          "适用人群": "通用",
          "使用方法": "口服",
          "国产/进口": "国产"
        """

        data_item["1星数"] = data['统计信息']['评分统计']['1星数']
        data_item["2星数"] = data['统计信息']['评分统计']['2星数']
        data_item["3星数"] = data['统计信息']['评分统计']['3星数']
        data_item["4星数"] = data['统计信息']['评分统计']['4星数']
        data_item["5星数"] = data['统计信息']['评分统计']['5星数']

        data_Excel.append(data_item)

    # 保存数据到JSON文件 以便查看
    saveJson(data_Excel, "汇总数据.json")
    print(f"数据量{len(data_Excel)}")
    # 转换好评数为整数 数据清洗
    for data in data_Excel:
        data['好评数'] = convert_to_integer(data['好评数'])

    # 转换为dataframe
    return DataFrame(data_Excel, index=None)


# 把包含所有数据的DataFrame保存为Excel文件
def DataFrame_all_To_Excel():
    df = Statistics_all_To_DataFrame()  # 获取DataFrame
    # 保存DataFrame为Excel文件
    df.to_excel('excel/全部数据4.xlsx', index=False)


"""
文件数据格式:
{
      "index": 1,
      "title": "舒尔佳 奥利司他胶囊0.12g*7粒",
      "ShopName": "鲁南舒尔佳京东自营官方旗舰店",
      "DetailsUrl": "https://item.jd.com/100011335310.html",
      "price": "49.90",
      "imgUrl": "https://img10.360buyimg.com/n7/jfs/t1/208650/1/41345/133144/66473282F1749056d/7430e4f34cb552e9.jpg",
      "统计信息": {
        "好评数": "25万+",
        "好评率": "96%",
        "差评": "5400+",
        "追评数": "4900+",
        "总评论数": "100万+",
        "评分统计": {
          "1星数": 5000,
          "2星数": 1000,
          "3星数": 2000,
          "4星数": 2000,
          "5星数": 200000
        },
        "商品信息": {
          "品牌信息": "舒尔佳",
          "商品名称": "舒尔佳奥利司他胶囊",
          "商品编号": "100011335310",
          "类别": "西药",
          "药品剂型": "胶囊剂",
          "适用人群": "通用",
          "使用方法": "口服",
          "国产/进口": "国产"
        }
      }
    }
"""

"""
由于不是一次性爬取所有数据，而是分批次爬取，
所以需要将爬取到的数据整合到一起，并保存到Excel文件中。
excel文件是很多的，所以需要将所有excel文件合并到一起。
"""


def 整合所有excel文件():
    # 指定目录路径
    directory = 'excel/'

    # 读取目录下的所有Excel文件
    all_dataframes = []
    length_list = []

    # 遍历目录下所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            filepath = os.path.join(directory, filename)
            df = pd.read_excel(filepath)
            # 统计每个DataFrame的长度
            length_list.append(len(df))
            all_dataframes.append(df)
            # all_dataframes 是所有dataframe的列表

    print(f"excel文件数量:{len(all_dataframes)}")
    print(length_list)
    print(f"总数: {sum(length_list)}")

    # 将所有DataFrame连接起来
    combined_df = pd.concat(all_dataframes, ignore_index=True)

    # 打印合并后的DataFrame
    print(combined_df)
    # 保存合并后的DataFrame为Excel文件
    combined_df.to_excel('汇总数据.xlsx', index=False)


if __name__ == '__main__':
    遍历文件夹的所有文件_然后一个一个重命名文件()
    统计所有文件的数据量()

    DataFrame_all_To_Excel()
    整合所有excel文件()

