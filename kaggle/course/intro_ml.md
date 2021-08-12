## pandas
A DataFrame holds the type of data you might think of as a table. This is similar to a sheet in Excel, or a table in a SQL database.


```python
import pandas as pd

# Path of the file to read
iowa_file_path = '../input/home-data-for-ml-course/train.csv'

# Fill in the line below to read the file into a variable home_data
home_data = pd.read_csv(iowa_file_path)

# What is the average lot size (rounded to nearest integer)?
avg_lot_size = round(home_data["LotArea"].mean())

y = home_data.SalePrice
```

How to select subset?

```python
# dropna drops missing values (think of na as "not available")
melbourne_data = melbourne_data.dropna(axis=0)

melbourne_features = ['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']
X = melbourne_data[melbourne_features]

X.describe()
X.head()

# format print
print(f"MAE Baseline Score: {baseline_score:.4}")
```

## Decision Trees

```python
from sklearn.tree import DecisionTreeRegressor

# Define model. Specify a number for random_state to ensure same results each run
melbourne_model = DecisionTreeRegressor(random_state=1)

# Fit model
melbourne_model.fit(X, y)


print("Making predictions for the following 5 houses:")
print(X.head())
print("The predictions are")
print(melbourne_model.predict(X.head()))
```

Model Validation

- [sklearn decision tree](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html)


- Overfitting
  - capturing spurious patterns that won't recur in the future, leading to less accurate predictions, or
- Underfitting
  - failing to capture relevant patterns, again leading to less accurate predictions.

```python
def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return(mae)
```

A deep tree with lots of leaves will overfit because each prediction is coming from historical data from only the few houses at its leaf.

many models have clever ideas that can lead to better performance. We'll look at the **random forest** as an example.






## English
You've built a model. But how good is it?

Measuring model quality is the key to iteratively improving your models.

### words

