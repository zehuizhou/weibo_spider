from snownlp import SnowNLP
import pandas as pd


def update_csv_row(csv_name):
    data = pd.read_csv(csv_name, encoding='utf_8_sig', )
    data[u'内容'] = data[u'内容'].astype(str)
    data[u'情感评分'] = data[u'内容'].apply(lambda x: SnowNLP(x).sentiments)
    data.to_csv(csv_name, index=False, encoding='utf_8_sig')


if __name__ == '__main__':
    update_csv_row('许可馨.csv')
