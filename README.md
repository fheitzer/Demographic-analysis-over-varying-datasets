# Demographic analysis over varying datasets
Datasets are different, but in their combined knowledge lies the truth.

## Context
The application context is demographic analysis which aims at measuring the dimensions and dynamics of (human) populations.
Here analysis methods have primarily been developed to study how populations of social actors can change across time
through a variety of processes, such as birth, death, and migration.

There exist a number of national and international statistics organizations (e.g., ISTAT, EUROSTAT, etc.) whose major
scope is to gather and study demographic data. Unfortunately, different organizations use different measuring methods.
In general, this leads to different publicly available data sets containing demographic information related to different
(partially overlapping) geographical regions, different time bounds, and different time granularity. Even in case of
same time window and same geographical region, different data sets may contain inconsistent values for the same process
(e.g., ISTAT and EUROSTAT might declare two different values for the population of Italy in 2005).


## Iteration 1 - Setting up
In this iteration I want to concentrate on cleaning the data I need, merging the dataframes and simply displaying it.
I am not trying to develop fancy interactive graphs and continuously updated data. I just want to get the program up and
running. I am concerned with the functions at their core so every planned feature must be implemented to have a running
program.

### Planned User Stories

#### Import, clean & merge datasets

<p align="center">
Check for the dataset for duplicate country/year combinations, if every column of interest is displayed and that the
year range is from 1950-2018. <br />
Estimated Time: 5 hours <br />
Priority: 10/10
</p>

#### Display data using the Bokeh

<p align="center">
Display the data. <br />
Estimated time: 4 hours <br />
Priority: 10/10
</p>


### Design choices

At first I implemented the algorithms in a Extreme Programming fashion. Not thinking too much about design patterns.
During the Refactoring process I determined and implemented certain design patterns. <br />

For the data gathering I kind of used a startegy approach. 

### Resumé

I implemented both user stories, but I wrote them in too much of a general fashion.
Therefore the estimated time was off and the clarity of how detailed the implementation is supposed to be was not given.
This is the reason why I took way too long to do the first Iteration and cannot do a second one.

## Iteration 2 - Improving modularity and maintainability

### Planned User Stories

#### Merge datapoints that represent the same country, but are written differently

<p align="center">
Check if "France (Metropolitan) is in the dataset<br />
Estimated Time: 1 hours <br />
Priority: 8/10
</p>

#### Add an interactive country List to view

<p align="center">
C. <br />
Estimated time: 4 hours <br />
Priority: 9/10
</p>


#### Add an interactive year range to view

<p align="center">
Look at the html. <br />
Estimated time: 4 hours <br />
Priority: 6/10
</p>

