from dotenv import load_dotenv
import os
import psycopg2


db_password = os.getenv('DB_PASSWORD')
db_username = os.getenv('DB_USER')
db_name = os.getenv('DB_NAME')

class ManageDatabase():
    def __init__(self, db_name, db_user, db_password):
        self.db_name =db_name
        self.db_user = db_user
        self.db_password = db_password
        self.conn = None
        self.cur = None
        self.tables = []
        self.scraped_tables = []
        self.api_tables = []
        self.dates = []
    
    def connect_database(self):
        self.conn = psycopg2.connect(dbname =self.db_name, user=self.db_user, password =self.db_password, host='localhost')
        self.cur = self.conn.cursor()
        
    def get_tables_dates(self):
        self.cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        self.tables = [row[0] for row in self.cur.fetchall()]
        self.scraped_tables = sorted([t for t in self.tables if t.startswith('spacex_webscrape_data')], reverse=True)
        self.api_tables = sorted([t for t in self.tables if t.startswith('spacex_api_data')], reverse=True)
        
       
        self.dates = ['_' + '_'.join(table.split('_')[-3:])
                      for table in self.api_tables
                    ]
    
    def clean_tables(self):
        for i, table in enumerate(self.api_tables):
            date_suffix = self.dates[i]
            api_table = self.api_tables[i]
            scraped_table = self.scraped_tables[i]
             
            self.cur.execute(f"""CREATE OR REPLACE VIEW api_trimmed{date_suffix} AS
            SELECT  
                flights,
                gridfins,
                reused,
                legs,
                landingpad,
                block,
                reusedcount,
                serial,
                CAST(date AS DATE) as date
            FROM   
                {api_table};
            """)

            self.cur.execute(f"""CREATE OR REPLACE VIEW scraped_casted{date_suffix} AS
            SELECT
                flight_no,
                launch_site,
                payload,
                payload_mass,
                orbit,
                customer,
                launch_outcome,
                version_booster,
                booster_landing,
                CAST(date AS DATE) AS date
            FROM
                {scraped_table};
            """)


            self.cur.execute(f"""CREATE OR REPLACE VIEW merged_launches{date_suffix} AS
            SELECT
                s.*,
                a.flights,
                a.gridfins,
                a.reused,
                a.landingpad,
                a.block,
                a.reusedcount,
                a.serial
            FROM
                scraped_casted{date_suffix} AS s
            LEFT JOIN api_trimmed{date_suffix} AS a
            ON s.date = a.date;
            """)

            self.cur.execute(f"""CREATE OR REPLACE VIEW merged_non_null{date_suffix} AS
            SELECT
                *
            FROM
            merged_launches{date_suffix}
            WHERE gridfins IS NOT NULL;
            """)

            self.cur.execute(f"""CREATE OR REPLACE VIEW merged_cleaned_booster{date_suffix} AS
            SELECT
                *
            FROM
            merged_non_null{date_suffix}
            WHERE TRIM(booster_landing) NOT IN ('No attempt', 'Uncontrolled', 'Precluded', 'No attempt\n');
            """)

            self.cur.execute(f"""CREATE OR REPLACE VIEW merged_cleaned{date_suffix} AS
            SELECT
                flight_no,
                launch_site,
                payload,
                payload_mass,
                orbit,
                customer,
                launch_outcome,
                version_booster,
                booster_landing,
                date,
                flights,
                gridfins,
                reused,
                block,
                reusedcount,
                serial,
                COALESCE(landingpad, 'LZ-1') AS landingpad
            FROM
                merged_cleaned_booster{date_suffix};
            """)
            
        self.conn.commit()
    
                
filter_tables = ManageDatabase(db_name, db_username, db_password)

filter_tables.connect_database()
filter_tables.get_tables_dates()
filter_tables.clean_tables()
    
        
            
        
    
     








