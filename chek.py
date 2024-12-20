import pandas as pd

df = pd.read_csv('dom_click.csv', delimiter=';', encoding='utf-8')
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)


print(df.head())

print(df.shape)

print(df.dtypes)



