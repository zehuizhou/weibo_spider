import pandas as pd


data = pd.date_range(start='20190714', end='20190827')
date_list = data.array
date_lists = []
for i in date_list:
    date_lists.append(str(i)[0:10])
print(date_lists)
