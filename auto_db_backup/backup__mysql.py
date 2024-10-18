import mysql.connector
from mysql.connector import Error
import click
import logging
from backup import sql_backup

def backupmysql(host, port, username, passwd,database_name, compress, notification, slack_token, channel_id, log, restore, backup_dir, csv_backup_format, tables, backup_file) -> None:
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
        connected = True
        # if restore
        if restore:
            try:
                with open(backup_file, 'r') as sql_file:
                    sql_commands = sql_file.read()
        
                    # Execute the SQL commands in the file
                    for command in sql_commands.split(';'):
                        if command.strip():
                            cursor.execute(command)

                    # Commit changes if needed (for INSERT, UPDATE, DELETE queries)
                    connection.commit()

                    # Close the cursor and connection
                    cursor.close()
                    connection.close()
                    click.echo("Databse file restored succesfully")
                    return
            except Exception as e:
                click.echo(f"Error occured : {str(e)}")

        if tables:
            total_tables = tables
            print(total_tables)
        else:
            cursor.execute("SHOW TABLES")
            total_tables = [i[0] for i in cursor.fetchall()]
            
        sql_backup(csv_backup_format, backup_dir, total_tables, database_name, cursor, notification, slack_token, channel_id, log)
                       
    except Error as e:
        click.echo(f"Error while connecting to MySQL: {e}")
        

    finally:
        if connected:
            connection.close()
            click.echo("MySQL connection closed")