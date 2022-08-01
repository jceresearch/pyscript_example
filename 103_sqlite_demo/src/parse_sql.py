import sqlite3
import pandas as pd


def print_table(file_name, table_name):
    with sqlite3.connect(file_name) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + table_name)
        for row in cursor.fetchall():
            print("Row:", row)


def sql_to_df(file_name, table_name):
    with sqlite3.connect(file_name) as con:
        df = pd.read_sql_query("SELECT * from " + table_name, con)
    return df

def df_to_sql(df, file_name, table_name="data"):
    with sqlite3.connect(file_name) as con:
        df.to_sql(table_name, con, if_exists="replace")
    return True