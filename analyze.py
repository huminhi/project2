import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter


def save_plot(plot_name):
    plt.savefig(plot_name)


def group_and_sum(dataframe, group_by):
    return dataframe.groupby(group_by).sum().reset_index()


def thousands(x, pos):
    return '%1.1fK' % (x * 1e-3)


# format to thousands in unit
formatter = FuncFormatter(thousands)


def create_axis_with_format():
    # plot permit against handgun and long_gun for each state
    fig, ax = plt.subplots(figsize=(10, 8))
    # apply thousand formatter
    ax.yaxis.set_major_formatter(formatter)
    return ax


# pandas dataframe output configs
desired_width = 200
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 30)

df = pd.read_csv("gun-data.csv")
# print out dataframe info
print(df.head())
print(df.shape)

# fill with O would make sense so we will not change value of total column
df.fillna(0, inplace=True)
print(df.info())
# extract year from month column
df['year'] = df['month'].str.extract(r'(\d+)-\d+', expand=True)
# group data with state and year columns and sum other columns
grouped_by_year_state = group_and_sum(df, ['year', 'state'])
# group data with state column only and sum other columns
states = group_and_sum(grouped_by_year_state, ['state']).sort_values('totals', ascending=False).head(5)['state']
# select top 5 states with most totals of permit checks and gun registrations
top_5_totals = grouped_by_year_state[grouped_by_year_state['state'].isin(states)]
top_5_totals.pivot(index='year', columns='state', values='totals').plot(title='Total gun checks/permits; Figure 1', ax=create_axis_with_format())
# save fig1 top 5 states with most totals of permit checks and gun registrations
save_plot('fig1.png')
# select top state that has most totals number
kentucky = grouped_by_year_state[grouped_by_year_state['state'] == 'Kentucky'].drop('totals', axis=1)
# save fig2
kentucky.plot(x='year', kind='area', stacked=True, ax=create_axis_with_format(), title='Gun check types in Kentucky; Figure 2')
save_plot('fig2.png')

# read census data
census_data = pd.read_csv("u.s.-census-data.csv")
# select Fact and top 5 state columns only
census_data = census_data.loc[:, ['Fact'] + list(states)]
# fill NaN columns with 0s
census_data = census_data.astype(object).replace(np.nan, 0)
# set index for dataframe
census_data.set_index('Fact', inplace=True)
# transpose census data
census_data = census_data.T.copy()
# rename columns
census_data.rename(columns={'Population estimates, July 1, 2016,  (V2016)': 'population',
                            'Housing units,  July 1, 2016,  (V2016)': 'housing'}, inplace=True)
# select population and housing column only
census_data = census_data.loc[:, ['population', 'housing']]
# replace commas in all columns
census_data.replace(',', '', regex=True, inplace=True)
census_data = census_data.astype(int)
# add year and state columns to census data
census_data['year'] = '2016'
census_data['state'] = census_data.index
# select data in 2016
top_5_2016 = top_5_totals[top_5_totals['year'] == '2016']
# join with census data
top_5_2016 = top_5_2016.set_index(['state', 'year']).join(census_data.set_index(['state', 'year']),
                                                          on=['state', 'year'], how='left', rsuffix='census')
# reset index to plot
top_5_2016 = top_5_2016.reset_index()
# plot population and permit for each state
top_5_2016.plot(x='state', y=['population', 'permit'], kind='bar', alpha=0.5, label=['population', 'permit'], ax=create_axis_with_format(), title='Population vs Gun Permits in 2016; Figure 3')
save_plot("fig3.png")

# plot top 5 states in terms of permit, handgun, long_gun and other
top_5_2016.plot(x='state', y=['permit', 'handgun', 'long_gun', 'other'], kind='bar', alpha=0.5, label=['permit', 'handgun', 'long_gun', 'other'], ax=create_axis_with_format(), title='Permit vs Handgun, Long Gun, and Other Firearms in 2016; Figure 4')
save_plot("fig4.png")

