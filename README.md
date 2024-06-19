# JinDong_spiders     # 京东减肥药爬虫程序

京东减肥药爬虫程序->Selenium、requests、xpath等库,使用Matplotlib、
excel等工具进行展示分析结果，使用关联规则分析挖掘数挖掘深层规律

## 运行顺序:
    在ini.py、data_ready.py 文件中配置登录信息,商品详情页cookies信息
1.根目录下运行start.py文件->开始爬取数据
2.运行 “统计” 目录下的index.py文件->生成统计报告
3.运行分析 “数据预处理” 目录下的 数据清洗.py 文件->生成数据清洗文件，最终文件: 数据预处理/备份/清洗后数据.xlsx
4.运行 “数据分析/matplotlib图” 目录下的index.py文件->生成数据分析图表
5.运行 “数据分析/关联规则分析” 目录下的index.py文件->生成关联规则分析报告

6.爬取的数据保存在 “data” 目录下的JSON文件中