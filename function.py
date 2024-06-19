"""
function.py: 一些常用的函数
"""
import re
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from PageProcessing import 页面滚动加载数据, getAllelement
from XiangQing import 获取商品评论统计信息
from ini import page_limit, 每个商品爬取间隔时间
from public import saveJson


def 获取当前页面的所有数据(driver: WebDriver, total_Data_Num: int, pages: int, pages_limit: int) -> bool:
    页面滚动加载数据(driver, 0.2)  # 页面滚动加载数据

    # 获取页面元素->解构赋值语法，它将函数返回的元素列表分配给了这些变量
    [ul_element, em_elements, img_elements, i_elements, a_elements, Shop_Owner_name_elements] = getAllelement(driver)

    index = 1  # 商品索引
    data = {}  # 存储数据
    data_list = []  # 存储数据列表

    cishu = 0
    # //*[@id="J_scroll_loading"]/span/a
    # //*[@id="J_scroll_loading"]/span/a/font
    if len(ul_element) != 60:
        while True:
            try:
                time.sleep(3)
                重试按钮 = driver.find_element(By.XPATH, '//*[@id="J_scroll_loading"]/span/a')
                cishu += 1
                重试按钮.click()
                print(f"单击重试按钮{cishu}...")
            except Exception as e:
                # 按钮不存在，说明加载完毕
                break

        [ul_element, em_elements, img_elements, i_elements, a_elements, Shop_Owner_name_elements] = getAllelement(
            driver)
        print("通过单击按钮后数据加载个数:", len(ul_element))

    record_num = 0  # 记录当前第几个商品
    # 数据获取 ,正常每一页有60个商品
    for em, img, i_element, a_element, Shop_Owner_name_element in zip(em_elements, img_elements, i_elements, a_elements,
                                                                      Shop_Owner_name_elements):
        title = em.text
        # print(f"{index} : {title}")
        item = {}
        # print(openElement(a_element))
        item = {
            'index': index,
            'title': title,
            'ShopName': Shop_Owner_name_element.get_attribute('title'),
            # 商品详情页链接
            'DetailsUrl': a_element.get_attribute('href'),
            'price': i_element.text,
            'imgUrl': img.get_attribute('src'),
        }

        # 使用正则表达式匹配数字部分  商品链接
        if re.search(r'\d+', a_element.get_attribute('href')):
            record_num += 1
            # 提取匹配到的数字部分
            productID = re.search(r'\d+', a_element.get_attribute('href')).group()
            print(f"开始爬取第{record_num}个商品ID:", productID)
        else:
            print("没有匹配到商品ID")

        time.sleep(每个商品爬取间隔时间)
        while True:
            item['统计信息'] = 获取商品评论统计信息(productId=productID, PageUrl=a_element.get_attribute('href'))
            if item['统计信息']:
                break  # 正常拿到数据，退出循环
            else:
                # 拿不到数据，就是cookie需要重新验证，京东后台没有给数据！
                print("获取评论数据失败，cookie需要重新验证,请手动拖动验证码！才能继续爬取！")
                # 去验证码验证cookie
                time.sleep(5)

        # print(item)
        data_list.append(item)
        index += 1

    data['data'] = data_list
    data['len'] = len(data_list)
    saveJson(data, filename=f'data//第{pages}页数据量{len(data_list)}.json')
    # 记录数据量
    total_Data_Num += len(data_list)
    print(f"数据总量:{total_Data_Num}")
    print("保存成功！！！！")

    # # 拉到底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)
    # 获取下一页的按钮
    NextPagesBtn = driver.find_element(By.XPATH, '//*[@id="J_bottomPage"]/span[1]/a[9]')
    NextPagesBtn.click()
    print("来到了下一页!!!")

    # 数据获取完毕，退出浏览器
    if pages == pages_limit:
        # 退出浏览器
        driver.quit()
        return False

    # 记录页码
    pages += 1
    # 刷新当前页面
    driver.refresh()
    time.sleep(3)

    print(f"当前页码:{pages}")

    # 页面页码: // *[ @ id = "J_bottomPage"] / span[2] / input
    # 初始化新的 WebDriver 对象
    获取当前页面的所有数据(driver, total_Data_Num, pages, page_limit)
