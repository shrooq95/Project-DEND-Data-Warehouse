import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

"""
    Extracts data from JSON files in S3 buckets and copies them to two staging tables using queries stored in 
    'copy_table_queries' stored in sql_queries.py
"""
    
def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

"""
    Transforms and loads data from the two staging tables to the dimensional model using the queries stored in  
    'insert_table_queries' stored in sql_queries.py
"""

def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()