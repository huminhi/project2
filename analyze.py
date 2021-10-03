import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# % matplotlib inline

# pandas dataframe output configs
desired_width = 200
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 30)

df = pd.read_csv("gun-data.csv")
print(df.head())
print(df.shape)

# fill with O would make sense so we will not change value of total column
df.fillna(0, inplace=True)
print(df.info())
df['year'] = df['month'].str.extract(r'(\d+)-\d+', expand=True)

grouped_by_year_state = df.groupby(['year', 'state']).sum().reset_index()
states = grouped_by_year_state.groupby('state').sum().reset_index().sort_values('totals', ascending=False).head(5)['state']
top_5_totals = grouped_by_year_state[grouped_by_year_state['state'].isin(states)]
top_5_totals.pivot(index='year', columns='state', values='totals').plot(figsize=(10, 8))
plt.savefig('fig1.png')

kentucky = grouped_by_year_state[grouped_by_year_state['state'] == 'Kentucky'].drop('totals', axis=1)
kentucky.plot(x='year', kind='area', stacked=True, figsize=(10, 8))
plt.savefig('fig2.png')
# plt.show()

