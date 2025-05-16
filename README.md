# **README File**

## **Project Title**

SpaceX Data Science Project (Python, PostgreSQL, Jupyter)

## **Introduction**

Welcome to my SpaceX Data Science Project. While completing the IBM Data Science course, many lessons focused on SpaceX launch data, but often with preprocessed, simplified CSVs. I wanted to take what I learned and apply it to a full end-to-end project using real-world SpaceX data and create a machine learning algorithm that can predict the success or failure of rocket booster re-landings.

This project pulls launch data from the SpaceX public API and scrapes additional data from the SpaceX Wikipedia page. It then builds a PostgreSQL database, flattens and stores nested data, performs data cleaning, exploratory data analysis (EDA), and finally trains a machine learning model to predict the success or failure of rocket booster landings.

## **Installation**

To install Project Title, follow these steps:

1. Install either [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution) to run environment
2. Steps if you want to be able to run script to create postgresDB and query the database
    - Download and install the latest version of PostgreSQL from the official site:  [PostgreSQL](https://www.postgresql.org/download/)
    - Note username, password, and port (default is 5432)
    - After installation run: **`psql --version`** (should see something like psql (PostgreSQL) 16.x)
    - In SQL shell run: **`createdb spacex_project_database`** Or use pgAdmin to create it via GUI.
    - Create and Configure a .ENV file in root directory with below variables:
        - DB_NAME=spacex_db
        - DB_USER=your_postgres_username
        - DB_PASSWORD=your_password 
3. Clone the Repository: **`https://github.com/rossmmorgan/SpaceX_Data_Science_Proj.git`**
3. to install Environment run: **`conda env create -f environment.yml`**
5. If you completed Step 2, you can run all scripts, including those that create and query the database. If you skipped Step 2, you can still run all notebooks and scripts that use the pre-generated .csv files instead of the database.  

## **Project Structure**

```
SpaceX_DataProject/
│
├── .env # Environment variables (excluded from version control)
├── .gitignore # Files and folders to ignore in Git
├── environment.yml # Conda environment configuration
├── README.md # Project overview and installation instructions
│
├── config/ # (Optional) Folder for configuration files
│
├── data/ # Contains both raw and cleaned data
│ ├── raw_data/ # .csv files from API and web scraping
│ └── clean_data/ # Cleaned .csv files used for EDA and modeling
│
├── scripts/ 
│ ├── pull_data/ # Scripts for API and web scraping
│ │ ├── api_data.py # Python class for pulling and storing API data as .csv
│ │ └── web_scraping.py # Python class for pulling and storing web-scraped data as .csv
│ ├── manage_database/ # Scripts to work with PostgreSQL database
│ │ ├── create_database.py # Python class for creating and uploading clean .csv file
│ │ └── clean_database.py # Python class for cleaning database with SQL
│ └── pycache/ 
│
├── notebooks/ # Jupyter notebooks for analysis and modeling
│ ├── EDA/
│ │ ├── eda_pandas.ipynb # EDA and data wrangling using pandas
│ │ └── eda_sql.ipynb # EDA and data wrangling using SQL
│ └── model_training/
│ └── model_training1.ipynb # Testing and training different ML models
│
├── models/ # Python scripts to train and evaluate models
│ └── decision_tree.py # Python class that trains and evaluates decision tree model
```

## **Usage**

1. Run api_data.py and web_scraping.py (located in scripts/pull_data/) to collect up-to-date SpaceX launch data and save it as .csv files.
2. Run create_database.py (in scripts/manage_database/) to create a PostgreSQL database and upload the raw .csv files.
3. Run clean_database.py to clean and normalize the database tables, and create SQL views for easier querying.
4. Open eda_pandas.ipynb and eda_sql.ipynb in the notebooks/EDA/ folder to perform exploratory data analysis (EDA) using both pandas and SQL.
5. run the entire eda_pandas.ipynb to upload a clean csv file for testing and training the model.
6. Navigate to the notebooks/model_training/ folder and open model_training1.ipynb to experiment with different machine learning models.
7. Run decision_tree.py in the models/ folder to train the final Decision Tree model and view evaluation metrics.

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## **Author**

Project Title was created by **[Ross Morgan](https://github.com/rossmmorgan)**.
