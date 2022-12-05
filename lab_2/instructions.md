# Cloud Computing for Distributed Big Data Applications - Practical Session 2

As you are all aware, Big Data and Cloud Computing are two distinct ideas, but the two
concepts are often crossed intricately together. Big Data refers to gigantic amounts of data
that can be structured, semi-structured or unstructured. 

It is usually collected from different
sources (eg., user input, sensors, sales data ..) for analytical purposes. The two main purposes
of collecting this data is to i) find relevant patterns that can be exploited later (eg., to build
statistical models) and ii) to process it in order to address some query. 

Your challenge today
(if you accept it :) ) is to dive deep into the data story-telling of one of two datasets that you
can download and choose from moodle.

## 1. Datasets

## 1.1 Global Warming Trends

This dataset by data science nonprofit Berkeley Earth reports on how land and
temperature vary by city (the bigger file) and by average on the planet. This
data is (mostly) already cleaned. The idea here is to dive deeper into global
surface temperature anomalies through your analysis. While doing so, please
document the different queries/ processing steps you thought of as well as the
results and observations that came out of those. You will be asked to return
them at the end of the course.

As a start you could run a sanity check (eg., unicity of the couple (country,
city) at a specific day, correspondence of the coordinates with the specified
city and country (to this end, you can use libraries like geopy), arbitrary
temperatures values), and anything relevant that comes to your mind.

In the following you will find some questions that might guide your analysis
but don’t stop at these!
1. Can global warming be observed on earth’s temperature evolution?

2. Can the average country temperature be plotted in a compact way? you
may take a (logical) sample of countries. You may also get the year’s
average temperature for each.

3. What does the comparison of the evolution of the temperature
between two drastically different countries (location wise) allow you to
observe?

4. Same question for cities

5. How does one specific country evolve between two distinct years?

6. Can the Arctic Ice Melting be observed by looking at the temperature
changes in northern cities?

7. Plot these cities in a map
8. Quantify the autocorrelation of the average temperature of the country
of your choice.

9. Is the temperature evolution of a northern city correlated with the
evolution of a southern one? a correlation heatmap could be
interesting.

10. Can cities be (manually) clusterized over their temperature?

## 1.2 London Crime Data

London is the capital and most populous city of England and the United
Kingdom. This data counts the number of crimes at two different geographic
levels of London (LSOA and borough) by year, according to crime type.
Includes data from 2008 to present. The idea is to explore the crime dataset,
define the most dangerous areas and visualize the data properly.
In the following you will find some questions that might guide your analysis
but don’t stop at these!

1. In what year was the highest number of crimes committed?
2. Over the years, which boroughs saw an INCREASE in crime
rate?
3. Which observed a DECREASE?
4. Are there any seasonal effects that are obvious in the data that
we might investigate?
5. What types of crimes are growing the fastest?
6. Study the autocorrelation between boroughs and crimes type

7. Plot the choropleth map based on the spatial crime rate

## 2. Athena, the analytics AWS service

Amazon Athena is a serverless interactive query service used to analyze and query data
stored in Amazon S3, JDBC and DynamoDB. It does that in standard SQL and it can tackle
well-known data formats such as CSV, JSON, Apache ORC, Avro, and Parquet and uses
standard SQL queries. _However, Athena is not includedin the free tier mode and you will get
chargedif you try to use it._ Instead of that, theidea of the exercise is that you i) get yourself
familiar with some functions of Athena (eg., querying a bucket with a Select, Updating a row,
batching multiple queries) and re-implement them by manipulating directly the bucket's client
interface.

The main steps are:

1. Create two S3 buckets : One to store the average temperature per country data, and an
    empty one for the results of the queries.
2. Get familiar with the following by reading the Boto3 Documentation on Athena:
a. Named queries : creation, deletion, batching, listing.
b. Prepared queries : creation, deletion, batching, listing and update.
c. Query execution : Start, Stop, Get...
3. Create three functions that query the data bucket and store the results in the results’
    bucket.


