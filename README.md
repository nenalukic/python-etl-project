# Weather Data ETL Pipeline

This repository contains an ETL (Extract, Transform, Load) pipeline that retrieves weather data from the OpenWeatherMap API, stores it in a PostgreSQL database, and uses Apache Airflow for orchestration.

## Pipeline Overview

The ETL pipeline performs the following steps:

1. Extract: The pipeline utilizes the OpenWeatherMap API to retrieve weather data for a specified location.
2. Transform: The extracted data is processed and transformed to ensure consistency and usability.
3. Load: The transformed data is stored in a PostgreSQL database for future analysis and visualization.

## Pipeline Orchestration

The pipeline is orchestrated using Apache Airflow, a platform for programmatically authoring, scheduling, and monitoring workflows. The Airflow DAG (Directed Acyclic Graph) defines the tasks and their dependencies, ensuring the proper execution order.

## Prerequisites

Before running the pipeline, make sure you have the following set up:

1. OpenWeatherMap API Key: Obtain an API key by creating an account on the [OpenWeatherMap website](https://openweathermap.org/) and generating an API key.
2. PostgreSQL Database: Set up a PostgreSQL database where the weather data will be stored.
3. Apache Airflow: Install and configure Apache Airflow according to the official documentation.

