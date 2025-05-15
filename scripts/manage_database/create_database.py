from dotenv import load_dotenv
import os
import glob
import psycopg2
from psycopg2 import sql
import re
import csv 


load_dotenv()

db_password = os.getenv('DB_PASSWORD')
db_username = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')

class CreateTable:
    def __init__(self, csv_path, db_password, db_username, db_name):
        self.csv_path = csv_path
        self.db_password = db_password
        self.db_username = db_username
        self.db_name = db_name
        self.cur = None
        self.conn = None
        
    def connect(self):
        self.conn = psycopg2.connect(
            host='localhost',
            port='5432',
            dbname=self.db_name,
            user=self.db_username,
            password=self.db_password
        )
        self.cur = self.conn.cursor()
        
    def normalize_column_name(self, col_name):
        col = col_name.strip().lower()
        col = re.sub(r'\s+', '_', col)
        col = re.sub(r'[^a-zA-Z0-9_]', '', col)
        return col
    
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
            
    def check_table_exists(self, table_check):
        query = sql.SQL('''SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = %s)''')
        self.cur.execute(query, (table_check,))
        exists = self.cur.fetchone()[0]
        return exists
        
        
    def create_table(self):
        for filename in glob.glob(os.path.join(self.csv_path,'*.csv')):
            table_name = os.path.basename(filename).replace('.csv', '').lower()
            print(f'processing: {table_name}')
            
            if self.check_table_exists(table_name):
                print(f"Table {table_name} exists, skipping creation")
                continue
            else:
            
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


spacex_database = CreateTable('raw_data', db_password, db_username, db_name)


spacex_database.connect()
spacex_database.create_table()
                
        