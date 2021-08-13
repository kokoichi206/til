# Pandas Tutorial
The Pandas course will give you the data manipulation skills to quickly go from conceptual idea to implementation in your data science projects. 

```python
import pandas as pd
```

- There are two core objects in pandas
  - the DataFrame
  - the Series.

## DataFrame
A DataFrame is a table. It contains an array of individual entries, each of which has a certain value.

```python
pd.DataFrame({'Yes': [50, 21], 'No': [131, 2]})

pd.DataFrame({'Bob': ['I liked it.', 'It was awful.'], 'Sue': ['Pretty good.', 'Bland.']})

fruit_sales = pd.DataFrame({'Apples':[35,41], 'Bananas': [21, 34]}, index=['2017 Sales', '2018 Sales'])

```

## Series
A Series, by contrast, is a sequence of data values. If a DataFrame is a table, a Series is a list. And in fact you can create one with nothing more than a list:

```python
pd.Series([1, 2, 3, 4, 5])
0    1
1    2
2    3
3    4
4    5
dtype: int64

quantities = ['4 cups', '1 cup', '2 large', '1 can']
items = ['Flour', 'Milk', 'Eggs', 'Spam']
ingredients = pd.Series(quantities, index=items, name='Dinner')
```

## Reading and Saving data files
```python
wine_reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv")
wine_reviews.shape

# すでにCSVにINDEXが入ってる場合！
wine_reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)
wine_reviews.head()

# Save file
animals.to_csv("cows_and_goats.csv")
```

loc and iloc

```python
reviews.iloc[-5:]
first_row = reviews.iloc[0]

indices = [1, 2, 3, 5, 8]
sample_reviews = reviews.loc[indices]

reviews.loc[:, ['taster_name', 'taster_twitter_handle', 'points']]

reviews.loc[reviews.country == 'Italy']

reviews.loc[(reviews.country == 'Italy') | (reviews.points >= 90)]

# isin
reviews.loc[reviews.country.isin(['Italy', 'France'])]

# notnull
reviews.loc[reviews.price.notnull()]

cols = ['country', 'province', 'region_1', 'region_2']
indices = [0, 1, 10, 100]
df = reviews.loc[indices, cols]

cols = ['country', 'variety']
df = reviews.loc[:99, cols]
```



