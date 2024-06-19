"""
:author: 罗邓
:date: 2024-05-10 14:50:00
:description: 此文件用于获取商品详情页的评论统计信息
"""

import json
import requests
from lxml import etree
from data_ready import *
from public import saveJson, getElementText, getPingLunUrl


def XiangQingPages(goods_Id):
    """
     :scription: 此方法返回详情页的评论统计信息
    :param goods_Id:
    :return:
    """
    url = url_XiangQingPages
    headers = {
        'Cookie': XiangQing_Cookie,
        'User-Agent': User_Agent
    }
    params = {
        'appid': 'item-v3',
        'functionId': 'pc_club_productCommentSummaries',
        'client': 'pc',
        'clientVersion': '1.0.0',
        't': '1715766114485',
        'body': f'{"referenceIds":"{goods_Id}","categoryIds":"9192,9193,12163","bbtf":"","shield":""}',
        'h5st': '20240515174154524%3Byz59gt6iymy5znn7%3Bfb5df%3Btk03w50431abb18n20B73qd0AjQ1S3n0DBhnl6UvQcDi6XaEsKJoBRe4GKYqBH2-0nvYGh59b1igP47htUdw6GRsfO_u%3Bbeb0264525ecaef7f02af559149cb637243a6054fe353928af5267fceb72f73f%3B4.7%3B1715766114524%3BVebQ_95cigmB0KaLsei9qb-GCg4-r_tAHpVjliDyQ10ZFh8qauTV-p_W7wGcGtxq23D54fNh6OQZCWA7WNSV1sSAk3mZvxhO33AP99y2eE_pvNFASnRJNijIr2hn2Fr8TNzlBn3riIaQgDpO0vBwzW3gcUHsqikjGmA0uiwZvQGq5Z1vll6w9THZdcUBQck-MLQXsVY9IuttPbuBVQxqWXmAJFtH095jLUE7lGez4Q7AjFNhQqUhLFTqBIubn9ROEZQy4Fc3DtdREtBjOPs49F8atP2GYdbP2mDkKKRVkhQClgx-qepe_FlAPuVuUj3lRSe3TpN5FtXUzPnSNaAQHgHw92Q7snQzaZs0TvgotVeko7NDvgtgWNd4k3fOnfZw33oRa5dQcUKllbpXNpjr2rV8hFlTjaqsU-MIPesVLjGz0m-P1ibRu-GZ_U-t2BECF4BIaNlVgv5Ua7oVq5EO5WvlWtKq3emqElsN3sHqaoZ0Xb5-FfX_1PZlbxVJRMFj31vuq7-sT_7NbFqvsCMK19N8fY_p5xIpUsrVxOLCu7nZggE7nDk8PeheJO0dl8zjLad9Prk3hGJ0DQIeqffFGvzEemLTD52YgeDqWQHLXbk3'
    }

    resp = requests.get(url=url, headers=headers, params=params)
    data = json.loads(resp.text)


def 获取商品所有评论(productId) -> bool:
    headers = {
        'Cookie': XiangQing_Cookie,
        'User-Agent': User_Agent
    }

    # 初始化 后面会改
    max_page = 100
    comments_List = []
    # 第一页有一点特殊 只有第一页给出了 评论统计信息
    resp = requests.get(url=getPingLunUrl(0, productId), headers=headers)
    data = json.loads(resp.text)
    print(data)
    # 获取最大页码数:
    max_page = data['maxPage']
    print(f"最大页码数:{max_page}")
    # 要返回的数据
    return_data = {
        "好评数": data['productCommentSummary']['goodCountStr'],
        "好评率": str(data['productCommentSummary']['goodRateShow']) + "%",
        "差评": data['productCommentSummary']['poorCountStr'],
        "追评数": data['productCommentSummary']['afterCountStr'],
        "总评论数": data['productCommentSummary']['commentCountStr'],
        "评分统计": {
            "1星数": data['productCommentSummary']['score1Count'],
            "2星数": data['productCommentSummary']['score2Count'],
            "3星数": data['productCommentSummary']['score3Count'],
            "4星数": data['productCommentSummary']['score4Count'],
            "5星数": data['productCommentSummary']['score5Count'],
        }
    }

    for comment in data['comments']:

        # 使用try-except语句来捕获KeyError异常->这是因为如果评论中不存在地理位置信息，尝试访问'location'键将引发此异常

        try:
            location = comment['location']
        except KeyError:
            location = "未知"

        comment_item = {
            "评论内容": comment['content'],
            "评论时间": comment['creationTime'],
            "位置": location,
            "评分星数": comment['score'],
        }
        print(f"位置:{location}")
        comments_List.append(comment_item)

    """
       第一页评论保存完毕
    """

    """
        不断完善评论表
    """
    current_page = 1
    while current_page <= max_page - 1:
        resp = requests.get(url=getPingLunUrl(current_page, productId), headers=headers)
        data = json.loads(resp.text)

        try:
            comments = data['comments']
        except KeyError:
            continue

        for comment in comments:
            try:
                location = comment['location']
            except KeyError:
                location = "未知"

            # 提取关键数据
            comment_item = {
                "评论内容": comment['content'],
                "评论时间": comment['creationTime'],
                "位置": location,
                "评分星数": comment['score'],
            }
            print(f"位置:{location}")
            comments_List.append(comment_item)
        current_page += 1

    return_data['comments_List'] = comments_List
    return_data['length'] = len(comments_List)
    # 评论保存
    saveJson(return_data, f"{productId} 评论数据采集.json")
    return True


# 使用xpath解析页面 获得商品信息
def 获取商品信息(PageUrl: str) -> None:
    # from 课设作业.function import getElementText
    headers = {
        'Cookie': XiangQing_Cookie,
        'User-Agent': User_Agent
    }
    resp = requests.get(url=PageUrl, headers=headers)
    html_text = resp.text.encode('utf-8')
    # 将字节转换为Unicode字符串，并使用utf-8解码
    element = etree.HTML(html_text.decode('utf-8'))

    # 有些商品没有商品信息，所以要用try-except语句来捕获IndexError异常
    try:
        # 获取品牌信息
        品牌信息 = element.xpath('//*[@id="parameter-brand"]/li/a/text()')[0]
    except IndexError:
        品牌信息 = "未知"
    #                           //*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]
    # 第二个ul 获取商品信息         //*[@id="detail"]/div[2]/div[1]/div[1]/ul
    # //*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]
    try:
        ul_element = element.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]')[0]
    except IndexError:
        ul_element = element.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul')[0]

    data_return = {
        "品牌信息": 品牌信息,
    }

    for li in ul_element:
        data_item = getElementText(li).strip().split('：')
        # print(data_item)
        data_return[str(data_item[0])] = str(data_item[1])
    # pprint.pprint(data_return)
    return data_return

    """
    获取返回数据：
            商品名称：痴宴酵素梅清肠排宿l便孝素梅子加强版酵素青梅果随便拉果零食 四十粒【酵素青梅】
            商品编号：10081515660779
            店铺： 宏格金智饮料店
            货号：10024286378669-宏饮料
            包装形式：袋装
            类别：青梅
            总净含量：≤200g
            国产/进口：国产
    """


# 获取商品信息("https://item.jd.com/10081515660779.html")
# 获取商品信息("https://item.jd.com/10081515660779.html")


# 此处可能会因为cookie过期而报错，需要手动验证码， cookie才能继续获取数据
def 获取商品评论统计信息(productId: str, PageUrl: str) -> dict:
    try:
        headers = {
            'Cookie': XiangQing_Cookie,
            'User-Agent': User_Agent
        }
        resp = requests.get(url=getPingLunUrl(0, productId), headers=headers)
        data = json.loads(resp.text)
        # 要返回的数据
        return_data = {"好评数": data['productCommentSummary']['goodCountStr'],
                       "好评率": str(data['productCommentSummary']['goodRateShow']) + "%",
                       "差评": data['productCommentSummary']['poorCountStr'],
                       "追评数": data['productCommentSummary']['afterCountStr'],
                       "总评论数": data['productCommentSummary']['commentCountStr'], "评分统计": {
                "1星数": data['productCommentSummary']['score1Count'],
                "2星数": data['productCommentSummary']['score2Count'],
                "3星数": data['productCommentSummary']['score3Count'],
                "4星数": data['productCommentSummary']['score4Count'],
                "5星数": data['productCommentSummary']['score5Count'],
            }, '商品信息': 获取商品信息(PageUrl)}
        # 获取商品的其他信息
        return return_data
    except Exception as e:
        print(e)
        return {}
