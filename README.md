# Datawarehouse Project
## Project description

Sparkify is a music streaming startup with a growing user base and song database. Their user activity and songs metadata data resides in json files in S3. 
The goal of the project is to build an ETL pipeline that will 
extracts data from S3 (Data storage),
stages them in Redshift (Data warehouse with columnar storage),
and transforms data into a set of dimensional tables for analytics team to continue finding insights in what songs their users are listening to.

## Data Sources

Data sources are provided by two public S3 buckets. 
Both buckets are JSON files
One bucket contains
Firstbucket has the information about songs and artists,
while the second has information concerning actions completed by users (which song are listening, etc.. ). 

The Redshift service is where data will be ingested and transformed, 
though COPY command we will access to the JSON files inside
the buckets and copy their content on our staging tables.

## ETL Pipeline
Project builds an ETL pipeline (Extract, Transform, Load) to create database and tables in AWS Redshift cluster, fetch data from JSON files stored in AWS S3, process the data, and insert the data to AWS Redshift database. (check out the sql_queries python module).

Project-3 uses python, SQL, AWS S3 and AWS Redshift DB.



