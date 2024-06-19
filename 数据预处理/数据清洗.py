import pprint
import pandas as pd
import numpy as np
from pandas import DataFrame
from public import saveJson

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


# 数据去重

def 数据去重():


    # 读取已经 保存的所有数据excel文件为DataFrame
    df = pd.read_excel('../统计/汇总数据.xlsx')

    # 统计重复值
    duplicate_rows = df[df.duplicated()]
    duplicate_count = len(duplicate_rows)
    print("统计重复信息如下；")
    print(duplicate_rows)
    print(f"共有{duplicate_count}条重复数据")

    # 去重
    df = df.drop_duplicates()
    # 备份数据
    df.to_excel('备份/去重后数据备份.xlsx', index=False)
    print(f"去重后数据长度:{df.shape[0]}")
    print(df.head())


def 格式化数据():
    """
    数据格式总是不一样的，需要对数据进行清洗，包括：
    1. 去除重复数据
    2. 缺失值处理
    3. 异常值处理
    :return:
    """

    """
    格式化的字段:
     好评率:整数
     差评：整数
     追评数:整数
     总评论数：整数    
    """
    # 读取已经 保存的去重所有数据excel文件为DataFrame
    df = pd.read_excel('备份/去重后数据备份.xlsx')
    print(df.head())
    # 将DataFrame转换为字典
    dict_data = df.to_dict(orient='records')

    # pprint.pprint(dict_data[0])

    for item in dict_data:
        # 处理差评
        if '+' in item['差评']:
            item['差评'] = item['差评'].replace('+', '')
            item['差评'] = int(item['差评']) + 1  # 减小 误差

        if '万' in item['追评数']:
            item['追评数'] = item['追评数'].replace('万', '')
            if '+' in item['追评数']:
                item['追评数'] = item['追评数'].replace('+', '')
                item['追评数'] = int(item['追评数']) + 1  # 减小 误差
                item['追评数'] = item['追评数'] * 10000
            else:
                item['追评数'] = int(item['追评数']) * 10000
        elif '+' in item['追评数']:
            item['追评数'] = item['追评数'].replace('+', '')
            item['追评数'] = int(item['追评数']) + 1  # 减小 误差

        if '万' in item['总评论数']:
            item['总评论数'] = item['总评论数'].replace('万', '')
            if '+' in item['总评论数']:
                item['总评论数'] = item['总评论数'].replace('+', '')
                item['总评论数'] = int(item['总评论数']) + 1  # 减小 误差
                item['总评论数'] = item['总评论数'] * 10000
            else:
                item['总评论数'] = int(item['总评论数']) * 10000
        elif '+' in item['总评论数']:
            item['总评论数'] = item['总评论数'].replace('+', '')
            item['总评论数'] = int(item['总评论数']) + 1  # 减小 误差

    # 数据格式转换完成，保存数据
    saveJson(dict_data, 'data.json')
    df = DataFrame(dict_data, index=None)
    print(df.head())
    # 保存清洗后的数据
    df.to_excel('备份/清洗后数据.xlsx', index=False)


def 统计缺失值():
    # 读取已经 保存的所有数据excel文件为DataFrame
    df = pd.read_excel('备份/清洗后数据.xlsx')
    # 统计缺失值
    missing_data = df.isnull().sum()
    print(missing_data)
    # 保存缺失值数据
    missing_data.to_excel('备份/缺失值统计.xlsx')



if __name__ == '__main__':
    数据去重()
    格式化数据()
    统计缺失值()
    # 最终数据保存在data.json文件、清洗后数据备份.xlsx文件
