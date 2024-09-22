import click
import os
import logging

# ANSI escape codes for colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"

# setting up the logging function show the errors
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger("colored_logger")


APP_VERSION = "1.0"

# Entry point for the command line interface (CLI)
@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show the version of the app and exit')
def cli(version):
    if version:
        click.echo(f"Auto_db_backup   {APP_VERSION}")

# Parameters to connect to the databse
def database_connection(func):
    func = click.option("--passwd", "-pw", required=True, help="Password of the database")(func)
    func = click.option("--database_name", "-db_name", required=True, help="Name of the database you want to backup")(func)
    func = click.option("--username", "-u", required=True, help="Username of the database")(func)
    func = click.option("--port", "-p", required=True, help="Port number of the database")(func)
    func = click.option("--host", "-h", required=True, help="The IP address of the database")(func)
    return func

# Flag to compress the backup files and during the restoring process to mention it is a compressed file
def compress(func):
    func = click.option("--compress", "-c", is_flag=True, help="Flag to enable for storing the files in a compressed format like gzip or tar")(func)
    return func

# Parameters to enable automatic backup process
def auto_backup(func):
    func = click.option("--auto_backup", "-ab", is_flag=True, default=False, help="flag to automate the backup process")(func)
    func = click.option("--frequency", required=False, type=click.Choice(["seconds", "minutes", "hours", "days"]), help="Frequency of the backup.")(func)
    func = click.option("--interval", required=False, default=1, help="Interval for the frequency (e.g., every 2 minutes)")(func)
    return func


# Parameters to store the backup files on the cloud
def storage_option(func):
    func = click.option("--storage_option", "-so", required=False, is_flag=True, help="Where to store the backup, in the cloud or local system")(func)
    func = click.option("--provider","-prov",required=False , type=click.Choice(["aws","gcp","azure"]), help="To backup the database to a cloud provider for (Example : AWS, GCP, AZURE.)")(func)
    return func

# Flag to enable slack notification services
def notification(func):
    func = click.option("--notification","-n", is_flag = True, help="To send slack notifications about the backup operations.")(func)
    func = click.option("--slack_token", required=False, help="Slack OAuth token for sending messages.")(func)
    func = click.option("--channel_id", required=False, help="Slack channel ID where notifications will be sent.")(func)
    return func

# To log the backup process into a log file
def logging_option(func):
    func = click.option("--logging", "-log", is_flag=True, help="Log the operations performed on the database and the timing of the backup")(func)
    return func

# to restore a database form a .sql file.
def restore_database(func):
    func = click.option("--restore", "-r", is_flag=True, help = "To restore a database to original format.")(func)
    func = click.option("--backup_file", required=False, help = "The backup file to restore the databse. It needs to be an .sql file")(func)
    return func

# backup directiry of the backup files folder and log file
def backup_dir(func):
    func = click.option('--backup_dir', default=f'{os.getcwd()}', hidden=True)(func)
    return func

# To backup from multiple tables in  a database for SQl databases
def tables_option(func):
    func = click.option("--tables", "-t", multiple=True, required=False, help="Specify tables to back up. Use multiple '-t table_name' for multiple tables.")(func)
    return func

# To backup the files in csv format you need to enable the this flag
def backup_format(func):
    func = click.option("--backup_format","-f", is_flag=True, required=False, type=click.Choice(["csv"], help= "By default the files are stored in SQL format for sql databses and JSON format for NOSQL databases, To backup the databse file into csv format."))
    return func

# To check wether all the required parameters are provided or not
def check_paramters(auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, restore, backup_file):
    flag = False
    if auto_backup and not (interval and frequency):
        logger.error(f"{RED}To enable auto backup --interval and --frequency arguments need to be provided.{RESET}")
        flag=True
    if storage_option and not provider:
        logger.error(f"{RED}To backup the files into cloud --provider arguments need to be provided.{RESET}")
        flag=True
    if notification and not (slack_token and channel_id):
        logger.error(f"{RED}To send slack messages --slack_token, --channel_id arguments need to be provided.{RESET}")
        flag=True
    if restore and not (backup_file): 
        logger.error(f"{RED}Backup file path is not provided for to restore.{RESET}")
        flag=True
    
    if not flag:
        return True

@click.command()
@database_connection
@compress
@auto_backup
@storage_option
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_mysql(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, logging, restore, backup_dir, backup_format, tables, backup_file):
    from backup__mysql import backupmysql
    res = check_paramters(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, restore, backup_file)
    if res:
        backupmysql(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, logging,restore, backup_dir, backup_format, tables, backup_file)
    


@click.command()
@database_connection
@compress
@auto_backup
@storage_option
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_postgresql(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, logging, restore, backup_dir, backup_format, tables, backup_file):
    from auto_db_backup.backup__postgresql import backuppostgresql
    res = check_paramters(auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, restore, backup_file)
    if res:
        pass


@click.command()
@database_connection
@compress
@auto_backup
@storage_option
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_sqlite3(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, logging, restore, backup_dir, backup_format, tables, backup_file):
    from auto_db_backup.backup__sqlite3 import backupsqlite3
    res = check_paramters(auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, restore, backup_file)
    if res:
        pass


@click.command()
@database_connection
@compress
@auto_backup
@storage_option
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_sqlserver(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, logging, restore, backup_dir, backup_format, tables, backup_file):
    from auto_db_backup.backup__sqlserver import backupsqlserver
    res = check_paramters(auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, restore, backup_file)
    if res:
        pass


@click.command()
@database_connection
@compress
@auto_backup
@storage_option
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_mariadb(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, logging, restore, backup_dir, backup_format, tables, backup_file):
    from auto_db_backup.backup__mariadb import backupmariadb
    res = check_paramters(auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, restore, backup_file)
    if res:
        pass


@click.command()
@database_connection
@compress
@auto_backup
@storage_option
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_oracledb(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, logging, restore, backup_dir, backup_format, tables, backup_file):
    from auto_db_backup.backup__oracledb import backuporacledb
    res = check_paramters(auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, restore, backup_file)
    if res:
        pass


@click.command()
@database_connection
@compress
@auto_backup
@storage_option
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_sybase(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, logging, restore, backup_dir, backup_format, tables, backup_file):
    from auto_db_backup.backup__sybase import backupsybase
    res = check_paramters(auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, restore, backup_file)
    if res:
        pass


@click.command()
@database_connection
@compress
@auto_backup
@storage_option
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_teradata(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, logging, restore, backup_dir, backup_format, tables, backup_file):
    from auto_db_backup.backup__teradata import backupteradata
    res = check_paramters(auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, restore, backup_file)
    if res:
        pass


@click.command()
@database_connection
@compress
@auto_backup
@storage_option
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@click.option("--collection_name","-col", multiple=True, required=False, help="Specify collections to back up. Use multiple '-col collection_name' for multiple collections.")
def backup_mongodb(host, port, username, passwd,database_name, compress, auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, logging, restore, backup_dir, backup_format, collection_name, backup_file):
    from auto_db_backup.backup__mongodb import backupmongodb
    res = check_paramters(auto_backup, interval, frequency, storage_option, provider, notification, slack_token, channel_id, restore, backup_file)
    if res:
        pass


cli.add_command(backup_mysql)
cli.add_command(backup_postgresql)
cli.add_command(backup_sqlite3)
cli.add_command(backup_sqlserver)
cli.add_command(backup_sybase)
cli.add_command(backup_oracledb)
cli.add_command(backup_mariadb)
cli.add_command(backup_mongodb)
cli.add_command(backup_teradata)

if __name__ == "__main__":
    cli()