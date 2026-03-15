# Shopify-ETL-Data-Pipeline
End-to-end Shopify ETL pipeline built with Python, MySQL, and Apache Airflow for automated data ingestion and transformation.


## Overview

This project implements an automated ETL (Extract, Transform, Load) pipeline that extracts product data from the Shopify API, processes the data using Python, and loads it into a MySQL database.

The pipeline is orchestrated using Apache Airflow to automate scheduling and execution.

This project demonstrates key data engineering concepts such as API ingestion, data transformation, workflow orchestration, and structured data storage.

---

## Problem Statement

E-commerce platforms such as Shopify generate large volumes of operational data through APIs. While this data is valuable for analytics, it is not always structured for reporting or downstream data analysis.

Without automation, engineers or analysts must manually extract and process data from the Shopify API, which is inefficient and error-prone.

This project solves that problem by building an automated pipeline that extracts Shopify product data, transforms it into a structured format, and stores it in a relational database for future analytics and reporting.

---

## Solution

The project implements an ETL pipeline that:

• Extracts product data from the Shopify API

• Stores raw API responses in a raw data table

• Transforms the data into structured records

• Loads processed data into staging and final tables

• Uses Apache Airflow to orchestrate and schedule the pipeline

• Logs pipeline activity for monitoring and debugging

---

## Architecture

Shopify API 

↓

Python Extraction Layer 

↓

Raw Data Table (MySQL) 

↓

Transformation Layer 

↓

Staging Table 

↓

Final Analytics Table 

↓

Apache Airflow Scheduler 


---

## Technologies Used

Python

Apache Airflow

MySQL

Shopify REST API

Logging

Environment Variables

---

## Pipeline Workflow

1. The pipeline sends a request to the Shopify API to retrieve product data.
2. Raw JSON responses are stored in the database.
3. Python transformation scripts clean and normalize the data.
4. Structured data is inserted into staging tables.
5. Final tables store analytics-ready product data.
6. Apache Airflow schedules and manages the pipeline execution.

---

## Environment Variables

To run this project locally, create a `.env` file in the project root.

Example:

SHOPIFY_SHOP=your-store.myshopify.com

SHOPIFY_TOKEN=your_shopify_access_token


MYSQL_USER=etl_user

MYSQL_PASSWORD=etl_password

MYSQL_DB=shopify_etl

Sensitive credentials are excluded from the repository for security.

---

## Pipeline DAG

![Airflow DAG](images/airflow_pipeline_A.png)


![Airflow DAG](images/airflow_pipeline_A.png)


![Airflow DAG](images/airflow_pipeline_A.png)

---

## Setup Instructions

1. Download the repository

    https://github.com/JoTM-stack/shopify-etl-pipeline.git

2. Navigate into the project

    shopify-etl-pipeline

3. Install dependencies

    pip install -r requirements.txt

4. Configure environment variables

    Create a `.env` file and add your Shopify credentials.

5. Start Apache Airflow

    airflow webserver -p 8080
   
    airflow scheduler

7. Trigger the DAG from the Airflow UI.

---

## Example Pipeline Execution

The pipeline runs as an Apache Airflow DAG that executes the ETL process automatically.

Airflow provides monitoring, logging, and scheduling capabilities to ensure reliable data ingestion.

---

## Author

Data Engineering Portfolio Project
