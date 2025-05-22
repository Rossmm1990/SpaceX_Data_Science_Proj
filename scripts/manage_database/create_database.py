from dotenv import load_dotenv
import os
import glob
import psycopg2
from psycopg2 import sql
import re
import csv

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
raw_data_path = os.path.join(base_dir, 'data', 'raw_data') 

load_dotenv()

db_password = os.getenv('DB_PASSWORD')
db_username = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')


# Class to create tables from all stored raw_data CSV files.
class CreateTable:
    def __init__(self, csv_path, db_password, db_username, db_name):
        self.csv_path = csv_path
        self.db_password = db_password
        self.db_username = db_username
        self.db_name = db_name
        self.cur = None
        self.conn = None
    
    # Connects to the database   
    def connect(self):
        self.conn = psycopg2.connect(
            host='localhost',
            port='5432',
            dbname=self.db_name,
            user=self.db_username,
            password=self.db_password
        )
        self.cur = self.conn.cursor()
        
    # Normalizes a column name by:
    # - Stripping whitespace and converting to lowercase
    # - Replacing spaces with underscores
    # - Removing all non-alphanumeric characters (except underscores)    
    
    def normalize_column_name(self, col_name):
        col = col_name.strip().lower()
        col = re.sub(r'\s+', '_', col)
        col = re.sub(r'[^a-zA-Z0-9_]', '', col)
        return col
    
    # Infers the appropriate SQL column type based on CSV values.
    def infer_column_type(self, values):
        try:
            for val in values:
                if val == '':
                    continue
                int(val)
            return 'INTEGER'
        except ValueError:
            try:
                for val in values:
                    if val =='':
                        continue
                    float(val)
                return 'FLOAT'
            except ValueError:
                return 'TEXT'
            
    # Checks if the given table name already exists in the database.        
    def check_table_exists(self, table_check):
        query = sql.SQL('''SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = %s)''')
        self.cur.execute(query, (table_check,))
        exists = self.cur.fetchone()[0]
        return exists
        
    # Creates and populates a table for each CSV file, using safe SQL formatting to define columns and avoid SQL injection.
    def create_table(self):
        
        # Scans all CSV files in the 'raw_data' folder located inside the 'data' directory
        for filename in glob.glob(os.path.join(self.csv_path,'*.csv')):
            table_name = os.path.basename(filename).replace('.csv', '').lower()
            print(f'processing: {table_name}')
            
            # Checks if a table already exists; if so, skips creation
            if self.check_table_exists(table_name):
                print(f"Table {table_name} exists, skipping creation")
                continue
            else:
                
                # Builds and executes a CREATE TABLE query using proper SQL formatting
                # - Extracts column names from each CSV, normalizes them, and infers SQL data types
                with open(filename, 'r', encoding='utf-8') as file:
                    create_query = sql.SQL('CREATE TABLE {table} (\n').format(
                        table=sql.Identifier(table_name)
                    )
                    reader = csv.DictReader(file)
                    header = reader.fieldnames
                    sample_data = [row for _, row in zip(range(20), reader)]
                    
                    types = []
                    
                    for col in header:
                        normalized_col = self.normalize_column_name(col)
                        values = [row[col] for row in sample_data if col in row]
                        inferred_type = self.infer_column_type(values)
                        types.append((normalized_col, inferred_type))
                        
                    columns = [
                        sql.SQL('{} {}').format(sql.Identifier(name), sql.SQL(dtype))
                        for name, dtype in types
                    ]              
                    create_query += sql.SQL(',\n').join(columns)
                    create_query += sql.SQL('\n)')
                    self.cur.execute("SELECT current_user;")
                    self.cur.execute(create_query)
                    self.conn.commit()
                    
                # Loads all rows from the CSV file into the newly created table
                with open(filename, 'r', encoding='utf-8') as f:  
                    copy_sql = sql.SQL("""
                        COPY {table} FROM STDIN WITH (FORMAT CSV, HEADER, DELIMITER ',', NULL '') 
                        """).format(table=sql.Identifier(table_name))
                    self.cur.copy_expert(copy_sql, f)
                    self.conn.commit()
                    self.cur.execute(sql.SQL("SELECT COUNT(*) FROM {table}").format(table=sql.Identifier(table_name)))
                    print(f"{table_name} now has {self.cur.fetchone()[0]} rows.")
            
        self.cur.close()
        self.conn.close()
        print('data successfuly uploaded')
        
    # Connects to the database, creates tables, and populates them with data
    def create_data_base(self):
        self.connect()
        self.create_table()
        
        
spacex_database = CreateTable(raw_data_path, db_password, db_username, db_name)


spacex_database.create_data_base()
                
        