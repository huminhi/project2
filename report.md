# REPORT #

### What data is used? ###

* [gun-data](https://d17h27t6h515a5.cloudfront.net/topher/2017/November/5a0a4db8_gun-data/gun-data.xlsx) from FBI's National Instant Criminal Background Check System (NICS).

### Investigation ###

* Which states (top 5) have most gun checks/registrations over years?

Below figure shows that California, Illinois, Kentucky, Pennsylvania, and Texas are the top 5 states that have the most gun checks/registrations over years.

![Figure 1](fig1.png "Figure 1")

* What are types of gun checks/registrations done in the top state?

From Figure 1, Kentucky seems to be top state that has highest gun check/registrations.
Below figure shows that permit checks takes the highest portion of gun checks followed by handgun registrations in Kentucky.

![Figure 2](fig2.png "Figure 2")

### Data wrangling done ###
* Since data has lots of null values, we have to fill in these cells. O-filling makes sense here because we dont want to make false sum of checks/registrations
* Extract year from month column and group data in year-wise will give better visualization.
* Group data in year and state to find out top 5 states (https://stackoverflow.com/questions/31569549/how-to-groupby-a-dataframe-in-pandas-and-keep-columns)
* Plot top 5 states (https://stackoverflow.com/questions/29233283/plotting-multiple-lines-in-different-colors-with-pandas-dataframe)
* Plot check/registration checks in top state to find out trend using area chart (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.area.html) 
