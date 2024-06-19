data = {
    "name": "Alice",
    "age": 30,
    "gender": "female"
}

# print(data.get('class', "123"))

import pandas as pd

data = [{'A': '123', 'B': '456'}, {'A': '555', 'B': '666'}, {'A': '123', 'B': '456'}, {'A': '123', 'B': '456'}]
df = pd.DataFrame(data)
print(df)

# 由df还原为原始的data
new_data = df.to_dict(orient='records')
print(new_data)
