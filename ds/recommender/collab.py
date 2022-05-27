from collections import Counter

import numpy as np
import pandas as pd

df = pd.read_csv("./test.csv")

N = df.userId.max()
M = df.movieId.max()

print("N, M")
print(N, M)

user_ids_count = Counter(df.userId)

n = 2

user_ids = [u for u, c in user_ids_count.most_common(n)]
print(user_ids)
