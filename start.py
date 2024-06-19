"""
author:zhangyu
date:2021/11/10
description:启动文件->启动浏览器->登录->获取数据->保存数据->关闭浏览器
"""
from selenium.webdriver.common.by import By
from data_ready import url4
import time
from selenium import webdriver
from function import 获取当前页面的所有数据
from ini import page_limit, password, username

# 实例化浏览器
driver = webdriver.Chrome()

# 实例:
driver.get(url=url4)
time.sleep(1)

# 找到输入框的位置，然后在这里写入
user_input = driver.find_element(by=By.XPATH, value='//*[@id="loginname"]')
pw_input = driver.find_element(by=By.XPATH, value='//*[@id="nloginpwd"]')
login_btn = driver.find_element(by=By.XPATH, value='//*[@id="formlogin"]/div[5]')

# 输入用户名和密码，点击登录
user_input.send_keys(username)
pw_input.send_keys(password)

login_btn.click()

# 暂停验证登录
time.sleep(10)

# 记录数据量
total_Data_Num = 0
# 记录页码
pages = 1
获取当前页面的所有数据(driver, total_Data_Num, pages,page_limit)
