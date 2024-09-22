import mysql.connector
from mysql.connector import Error
import click
import logging

def backupmysql(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, log, restore, backup_dir, tables, backup_file) -> None:
    connected = False
    try:
        # Creating a connection to the databse
        connection = mysql.connector.connect(
            host=f'{host}',          
            user=f'{username}',      
            password=f'{passwd}',  
            database=f'{database_name}',
            port=int(port)
        )
        
        cur = connection.cursor()
        
        if tables:
            total_tables = tables
            print(total_tables)
        else:
            cur.execute("SHOW TABLES")
            res = cur.fetchall()
            total_tables = res
            print(total_tables)
        
        
        

    except Error as e:
        click.echo(f"Error while connecting to MySQL: {e}")

    finally:
        if connected:
            connection.close()
            click.echo("MySQL connection closed")