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
Display the returned dataset, check for duplicate country/year combinations, if every column of interest is displayed. <br />
Estimated Time: 5 hours <br />
Priority: 10/10
</p>

#### Display data using the Bokeh





## Iteration 2 - Improving maodularity and maintainability