import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决符号显示异常


def Get_Data_DataFrame():
    # 读取已经 保存的所有数据excel文件为DataFrame
    df = pd.read_excel('../../数据预处理/备份/清洗后数据.xlsx')
    return df


def 商品价格区间柱状图():
    # 获取数据DataFrame
    df = Get_Data_DataFrame()

    # 所爬取的数据中 ，最高价格为 3065

    # 区间范围
    bins = [1, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000]

    # 将值划分到不同的区间并统计每个区间的数量
    df['Bin'] = pd.cut(df['price'], bins=bins)
    counts = df['Bin'].value_counts().sort_index()

    # 创建图表对象并设置大小
    fig = plt.figure(figsize=(16, 14))

    # 绘制区间柱状图
    bars = plt.bar(counts.index.astype(str), counts.values)

    # 在每个柱子上显示数据标签
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, yval, ha='center', va='bottom')

    plt.xlabel('价格区间', fontsize=20)  # 设置X轴标签
    plt.ylabel('商品个数', fontsize=20)  # 设置Y轴标签
    plt.title('商品价格区间柱状图', fontsize=40)  # 设置标题

    # 显示图表
    plt.show()
    # 保存图表
    return fig.savefig('商品价格区间柱状图.png')


def 药品剂类图_柱状图():
    # 获取数据DataFrame
    df = Get_Data_DataFrame()

    # 统计某一列数据的出现次数
    value_counts = df['药品剂型'].value_counts()

    # 生成柱状图
    fig1 = plt.figure(figsize=(8, 6))
    bars = plt.bar(value_counts.index, value_counts.values)
    plt.xlabel('药品剂型', fontsize=20)
    plt.ylabel('个数', fontsize=20)
    plt.title('药品剂类柱状图', fontsize=30)

    # 在每个柱子上方显示对应的数值
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom')

    # 显示柱状图
    plt.show()
    fig1.savefig('药品剂类图_柱状图.png')


def 药品剂类图_饼图():
    # 获取数据DataFrame
    df = Get_Data_DataFrame()

    # 统计某一列数据的出现次数
    value_counts = df['药品剂型'].value_counts()
    # 生成饼图
    fig2 = plt.figure(figsize=(8, 8))
    plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%')
    plt.title('药品剂类图_饼图', fontsize=30)
    # 显示饼图
    plt.show()
    fig2.savefig('药品剂类图_饼图.png')


def 商品类别图():
    df = Get_Data_DataFrame()
    # 统计某一列数据的出现次数
    value_counts = df['类别'].value_counts()
    # 生成饼图
    fig2 = plt.figure(figsize=(8, 8))
    plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%')
    plt.title('商品类别图', fontsize=30)
    # 显示饼图
    plt.show()
    fig2.savefig('商品类别图_饼图.png')


if __name__ == '__main__':
    商品价格区间柱状图()
    药品剂类图_饼图()
    药品剂类图_柱状图()
    商品类别图()
    pass
