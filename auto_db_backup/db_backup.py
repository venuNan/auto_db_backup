import mysql.connector
from mysql.connector import Error
import csv
import subprocess
import schedule
import datetime
import os
import gzip
import click
import logging

def auto_backup():
    pass



def backup(rows, description, database_name, table, compress, storage_option, logging, backup_dir):
    if not os.path.exists("Database_backup_files"):
        os.mkdir("Database_backup_files")

    # Get the column names from the cursor description
    column_headers = [i[0] for i in description]

    # Time to use in the csv file when it was created
    now = datetime.datetime.now().strftime("%Y-%m-%d")

    # Creates a CSV file and writing exach table into a csv file names starting with the databse name follwed by table name and time of backup
    if compress:
        filename = os.path.join(backup_dir, f"Database_backup_files/{database_name}_{table}_{now}.gz")

        # Ensure the file does not already exist by adding a counter if necessary
        counter = 1
        while os.path.exists(filename):
            filename = os.path.join(backup_dir, f"Database_backup_files/{database_name}_{table}_{now}_{counter}.gz")
            counter += 1
        with gzip.open(f"{filename}", mode='wt', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_headers)
            writer.writerows(rows)
        click.echo(f"File has been saved into {filename}")


    else:
        filename = os.path.join(backup_dir, f"Database_backup_files/{database_name}_{table}_{now}.csv")

        # Ensure the file does not already exist by adding a counter if necessary
        counter = 1
        while os.path.exists(filename):
            filename = os.path.join(backup_dir, f"Database_backup_files/{database_name}_{table}_{now}_{counter}.csv")
            counter += 1
        with open(f"{filename}", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_headers)
            writer.writerows(rows)
        click.echo(f"File has been saved into {filename}")
        
def backup_mysql(host, username, passwd, database_name, tables, compress, storage_option, logging, auto_backup, backup_dir, port_no=3306):
    connected = False
    try:
        # Creating a connection to the databse
        connection = mysql.connector.connect(
            host=f'{host}',          
            user=f'{username}',      
            password=f'{passwd}',  
            database=f'{database_name}',
            port=port_no
        )

        if connection.is_connected():
            connected=True
            print("Connected to MySQL database")

        # Create a cursor object to interact with the database
        cur = connection.cursor()

        # If specific tables are provided, use them; otherwise, fetch all tables
        if tables:
            total_tables = tables
        else:
            cur.execute("SHOW TABLES")
            total_tables = [table[0] for table in cur.fetchall()]

         # Loop through each table and export its content to a CSV file
        for table in total_tables:
            print(f"Exporting {table}...")

            # Extracting each table from the database
            cur.execute(f"SELECT * FROM {table}")
            rows = cur.fetchall()
            # Extracting the description to ge the table column names
            description = cur.description
            
            backup(rows, description, database_name, table, compress, storage_option, logging, backup_dir)

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        

    finally:
        if connected:
            connection.close()
            print("MySQL connection closed")

def backup_postgresql(host, port, username, passwd, compress, storage_option, logging, auto_backup):
    pass

def backup_sqlite3(host, port, username, passwd, compress, storage_option, logging, auto_backup):
    pass

def backup_sqlserver(host, port, username, passwd, compress, storage_option, logging, auto_backup):
    pass

def backup_mariadb(host, port, username, passwd, compress, storage_option, logging, auto_backup):
    pass

def backup_oracledb(host, port, username, passwd, compress, storage_option, logging, auto_backup):
    pass

def backup_sybase(host, port, username, passwd, compress, storage_option, logging, auto_backup):
    pass

def baackup_teradata(host, port, username, passwd, compress, storage_option, logging, auto_backup):
    pass

def baackup_mongodb(host, port, username, passwd, compress, storage_option, logging, auto_backup):
    pass