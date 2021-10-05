import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# % matplotlib inline


def save_plot(plot_name):
    plt.savefig(plot_name)


def group_and_sum(dataframe, group_by):
    return dataframe.groupby(group_by).sum().reset_index()


# pandas dataframe output configs
desired_width = 200
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 30)
figsize = (10, 8)

df = pd.read_csv("gun-data.csv")
print(df.head())
print(df.shape)

# fill with O would make sense so we will not change value of total column
df.fillna(0, inplace=True)
print(df.info())
df['year'] = df['month'].str.extract(r'(\d+)-\d+', expand=True)

grouped_by_year_state = group_and_sum(df, ['year', 'state'])
states = group_and_sum(grouped_by_year_state, ['state']).sort_values('totals', ascending=False).head(5)['state']
top_5_totals = grouped_by_year_state[grouped_by_year_state['state'].isin(states)]
top_5_totals.pivot(index='year', columns='state', values='totals').plot(figsize=figsize)
save_plot('fig1.png')

kentucky = grouped_by_year_state[grouped_by_year_state['state'] == 'Kentucky'].drop('totals', axis=1)
kentucky.plot(x='year', kind='area', stacked=True, figsize=figsize)
save_plot('fig2.png')
# plt.show()
