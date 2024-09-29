import mysql.connector
from mysql.connector import Error
import click
import logging
import os
import datetime
from storage_option import local_backup,cloud_backup

def backupmysql(host, port, username, passwd,database_name, compress, storage_option, provider, notification, slack_token, channel_id, log, restore, backup_dir, csv_backup_format, tables, backup_file) -> None:
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
        
        cursor = connection.cursor()
        
        if tables:
            total_tables = tables
            print(total_tables)
        else:
            cursor.execute("SHOW TABLES")
            total_tables = [i[0] for i in cursor.fetchall()]
            print(total_tables)
        if restore
        if storage_option:
            cloud_backup(provider, )
        else:
            local_backup(csv_backup_format, backup_dir, total_tables, database_name, cursor, csv_backup_format, notification, slack_token, channel_id, log, )
                       
    except Error as e:
        click.echo(f"Error while connecting to MySQL: {e}")

    finally:
        if connected:
            connection.close()
            click.echo("MySQL connection closed")