import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df1 = pd.read_csv('output/tbl_dataset.clusDStart--clusDStart.csv')
df1[np.isfinite(df1['clusDStart'])].hist(column='clusDStart', bins=10)

plt.show()

df2 = pd.read_csv('output/tbl_dataset.clusNHits--clusNHits.csv')
df2[np.isfinite(df2['clusNHits'])].hist(column='clusNHits', bins=10)

plt.show()
