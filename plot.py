import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('output/tbl_dataset.deltaStart--clusters.csv')

df[np.isfinite(df['deltaStart'])].hist(column='deltaStart', bins=10)

plt.show()
