"""
:解释:此模块用于处理页面数据，包括获取页面元素，页面滚动加载数据
:页面处理模块
:author: 罗邓
:date: 2021-05-11
"""

import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def getAllelement(driver: WebDriver) -> list:
    ul_element = driver.find_elements(By.XPATH, '//*[@id="J_goodsList"]/ul/li/div/div[3]/a/em')
    print(f"商品数:{len(ul_element)}")
    # 获取所有em em里有商品标题                           //*[@id="J_goodsList"]/ul/li[1]/div/div[3]/a/em
    em_elements = driver.find_elements(By.XPATH, '//*[@id="J_goodsList"]/ul/li/div/div[3]/a/em')
    # 获取所有 价格元素            //*[@id="J_recommendGoods"]/div[2]/ul/li/div[2]/strong/i 特殊 推荐的商品！
    i_elements = driver.find_elements(By.XPATH, '//*[@id="J_goodsList"]/ul/li/div/div[2]/strong/i')
    # 获取所有图片 //*[@id="J_goodsList"]/ul/li[1]/div/div[1]/a/img
    img_elements = driver.find_elements(By.XPATH, '//*[@id="J_goodsList"]/ul/li/div/div[1]/a/img')
    # 获取详情链接 元素
    a_elements = driver.find_elements(By.XPATH, '//*[@id="J_goodsList"]/ul/li/div/div[1]/a')
    # 获取店家信息
    Shop_Owner_name_elements = driver.find_elements(By.XPATH, '//*[@id="J_goodsList"]/ul/li/div/div[5]/span/a')

    return [ul_element, em_elements, img_elements, i_elements, a_elements, Shop_Owner_name_elements]


def 页面滚动加载数据(driver: WebDriver, scroll_delay=0.5) -> None:
    """
    解释: 页面滚动加载数据，直到页面底部，再次滚动到页面中部，获取所有商品数据
    :param driver: WebDriver对象
    :param scroll_delay: 滚动时间间隔，单位为秒，默认0.5秒
    :return: None
    :time: 2024-06-2 10:50:00
    :author: 罗邓
    """

    # 获取页面的初始高度
    prev_height = driver.execute_script("return document.body.scrollHeight")
    print(f"页面高度: {prev_height}")
    # 设置慢慢拉动的时间间隔（单位为秒）

    # 持续滚动直到滚动到页面底部
    curr_height = 0

    # 下面两个while循环是为了拉到底部，因为页面加载后，页面底部的元素可能还没加载出来，所以需要循环下拉
    while True:
        # 拉动浏览器窗口一点点向下滚动
        driver.execute_script("window.scrollBy(0, 1000);")
        # 等待一段时间
        time.sleep(scroll_delay)
        # 获取当前滚动后的页面高度  driver.execute_script("return document.body.scrollHeight")
        curr_height += 1000
        print(f"当前高度: {curr_height},页面高度: {prev_height}")
        # 如果两次滚动之后的页面高度相同，即已经滚动到页面底部，则终止循环
        if curr_height >= prev_height:
            break

    while True:
        # 拉动浏览器窗口一点点向下滚动
        driver.execute_script("window.scrollBy(0, -1000);")
        # 等待一段时间
        time.sleep(scroll_delay)
        # 获取当前滚动后的页面高度  driver.execute_script("return document.body.scrollHeight")
        curr_height -= 1000
        print(f"当前高度: {curr_height},页面高度: {prev_height}")
        # 如果两次滚动之后的页面高度相同，即已经滚动到页面底部，则终止循环
        if curr_height <= prev_height / 1.5:
            break
    # 等待数据加载
    time.sleep(3)
