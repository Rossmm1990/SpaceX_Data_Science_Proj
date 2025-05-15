# **README File**

## **Project Title**

SpaceX Data Science Project (Python, PostgreSQL, Jupyter)

## **Introduction**

Welcome to my SpaceX Data Science Project. While completing the IBM Data Science course, many lessons focused on SpaceX launch data, but often with preprocessed, simplified CSVs. I wanted to take what I learned and apply it to a full end-to-end project using real-world SpaceX data and create a machine learning algorithm that can predict the success or failure of rocket booster re-landings.

This project pulls launch data from the SpaceX public API and scrapes additional data from the SpaceX Wikipedia page. It then builds a PostgreSQL database, flattens and stores nested data, performs data cleaning, exploratory data analysis (EDA), and finally trains a machine learning model to predict the success or failure of rocket booster landings.

## **Installation**

To install Project Title, follow these steps:

1. Install either [Download Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Download Anaconda](https://www.anaconda.com/products/distribution) to run environment
2. Steps if you want to be able to run script to create postgresDB and query the database
    a. Download and install the latest version of PostgreSQL from the official site:  [Download PostgreSQL](https://www.postgresql.org/download/)
    b. Note username, password, and port (default is 5432)
    c. After installation run: **`psql --version`** (should see something like psql (PostgreSQL) 16.x)
    d. In SQL shell run: **`createdb spacex_project_database`** Or use pgAdmin to create it via GUI.
    e. Create and Configure a .ENV file in root directory with below variables:
        - DB_NAME=spacex_db
        - DB_USER=your_postgres_username
        - DB_PASSWORD=your_password 
3. Clone the Repository: **`https://github.com/rossmmorgan/SpaceX_Data_Science_Proj.git`**
3. to install Environment run: **`conda env create -f environment.yml`**
5. If you completed Step 2, you can run all scripts, including those that create and query the database. If you skipped Step 2, you can still run all notebooks and scripts that use the pre-generated .csv files instead of the database.  
