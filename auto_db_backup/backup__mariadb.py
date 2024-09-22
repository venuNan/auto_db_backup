import mariadb
import click

def backupmariadb(host:str, username:str, passwd, database_name:str, compress:bool, storage_option: str, logging:bool, port_no:int=3306) -> None:
        # Connect to MariaDB Platform
        try:
            connection = mariadb.connect(
                user=username,
                password=passwd,
                host=host,
                port=port_no,
                database=database_name

            )
            
        except mariadb.Error as e:
            connection.close()
            click.echo(f"Error connecting to MariaDB Platform: {e}")
            
