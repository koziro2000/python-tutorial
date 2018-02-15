import datetime
import numpy as np
import pandas as pd

numRows = 25
df1 = pd.DataFrame(np.random.rand(numRows, 3), columns=list('ABC'))
df2 = df1.copy()

df1.head()

numDiscrepancies = 4
for row in range(numDiscrepancies):
    df1.iloc[len(df1.index)-row-1, 1] = np.random.rand(1)
    
removeNrows = 3
drop_indices = np.random.choice(df2.index, removeNrows, replace=False)
df2 = df2.drop(drop_indices)

numDuplications = 3
def duplicateSomeRows(df, numrows):
    for row in range(numrows):
        df = df.append(df.iloc[row])
    df.index = range(len(df.index))
    return df

df1 = duplicateSomeRows(df1, numDuplications)
df2 = duplicateSomeRows(df2, numDuplications-2)

df1['gr'] = df1.groupby(['A','B', 'C'])['A'].transform('count')
df1.head()


df2['gr'] = df2.groupby(['A','B', 'C'])['A'].transform('count')
df2.head()