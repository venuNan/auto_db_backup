import mariadb
import click

def backupmariadb(host, port, username, passwd, database_name, compress, storage_option, provider, notification, slack_token, channel_id, logging,restore, backup_dir, csv_backup_format, tables, backup_file) -> None:
        # Connect to MariaDB Platform
        try:
            connection = mariadb.connect(
                user=username,
                password=passwd,
                host=host,
                port=port,
                database=database_name
            )

            cur = connection.cursor()
            
        except mariadb.Error as e:
            connection.close()
            click.echo(f"Error connecting to MariaDB Platform: {e}")
            
