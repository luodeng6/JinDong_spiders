from 数据分析.matplotlib图.index import Get_Data_DataFrame
def 关联分析():
    from mlxtend.preprocessing import TransactionEncoder
    from mlxtend.frequent_patterns import apriori, association_rules
    import pandas as pd

    # 创建一个包含交易记录的列表
    data_list = Get_Data_DataFrame().to_dict(orient='records')
    data = []
    # 转换数据格式
    for item in data_list:
        list = [str(item["ShopName"])]
        if item["price"] < 50:
            list.append("0-50元")
        elif item["price"] < 100:
            list.append("50-100元")
        elif item["price"] < 200:
            list.append("100-200元")
        elif item["price"] < 300:
            list.append("200-300元")
        elif item["price"] < 400:
            list.append("300-400元")
        elif item["price"] < 500:
            list.append("400-500元")
        elif item["price"] < 1000:
            list.append("500-1000元")
        elif item["price"] < 2000:
            list.append("1000-2000元")
        elif item["price"] < 3000:
            list.append("2000-3000元")
        elif item["price"] < 4000:
            list.append("3000-4000元")

        list.append(str(item["品牌信息"]))
        list.append(str(item["类别"]))
        list.append(str(item["药品剂型"]))
        list.append(str(item["适用人群"]))
        list.append(str(item["使用方法"]))
        list.append(str(item["国产/进口"]))

        if item["好评率"] > 90:
            list.append("好评多数")
        else:
            list.append("好评少数")

        data.append(list)

    # 转换数据为适合Apriori算法的格式
    te = TransactionEncoder()
    te_ary = te.fit_transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # Apriori算法找出频繁项集   调整min_support参数可以调整关联规则的准确性
    frequent_itemsets = apriori(df, min_support=0.6, use_colnames=True)

    # 根据频繁项集->关联规则
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.8)

    # 频繁项集、关联规则
    print("频繁项集：")
    print(frequent_itemsets)

    print("\n关联规则：")
    """
    antecedents：表示关联规则的前项，即规则的条件部分。
    consequents：表示关联规则的后项，即规则的结果部分。
    antecedent support：表示前项的支持度，即数据集中包含前项的比例。
    consequent support：表示后项的支持度，即数据集中包含后项的比例。
    support：表示规则的支持度，即数据集中同时包含前项和后项的比例。
    """

    # 输出更多的行和列，不被限制
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(rules)

    print("--------------")
    print("关联规则可视化")
    print(rules)


if __name__ == '__main__':
    关联分析()
