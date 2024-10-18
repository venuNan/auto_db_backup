import click
import os
import logging
from pathlib import Path


# ANSI escape codes for colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"

# setting up the logging function show the errors
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# version of the python package
APP_VERSION = "1.0"

# Entry point for the command line interface (CLI)
@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show the version of the app and exit')
def cli(version):
    if version:
        click.echo(f"Auto_db_backup   {APP_VERSION}")

# Parameters to connect to the databse
def database_connection(func):
    func = click.option("--password", "-pw", required=True, help="Password of the database")(func)
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
    func = click.option("--auto_backup", "-ab", is_flag=True, help="Automate the backup process")(func)
    func = click.option("--frequency", required=False, type=click.Choice(["seconds", "minutes", "hours", "days"]), help="Frequency of the backup.")(func)
    func = click.option("--interval", required=False, help="Interval for the frequency (e.g., every 2 minutes)")(func)
    return func


# Flag to enable slack notification services
def notification(func):
    func = click.option("--notification", "-n", is_flag = True, help="To send slack notifications about the backup operations.")(func)
    func = click.option("--slack_token", "-st", required=False, help="Slack OAuth token for sending messages.")(func)
    func = click.option("--channel_id", "-ci", required=False, help="Slack channel ID where notifications will be sent.")(func)
    return func

# Flag to log the backup process into a log file
def logging_option(func):
    func = click.option("--logging", "-log", is_flag=True, help="Log the operations performed on the database and the timing of the backup")(func)
    return func


# To restore a database form a .sql file.
def restore_database(func):
    func = click.option("--restore", "-r", is_flag=True, help="Restore a database from a backup")(func)
    func = click.option("--backup_file", required=False, help = "The backup file to restore the databse. It needs to be an .sql file")(func)
    return func


# backup directiry of the backup files folder and log file
def backup_dir(func):
    func = click.option('--backup_dir', default=f'{Path.home()}', hidden=True)(func)
    return func


# To backup from multiple tables in  a database for SQl databases
def tables_option(func):
    func = click.option("--tables", "-t", multiple=True, required=False, help="Specify tables to back up. Use multiple '-t table_name1 -t table_name2' for multiple tables.")(func)
    return func


# To backup the files in csv format you need to enable the this flag
def backup_format(func):
    func = click.option("--csv_backup_format", "-cf", is_flag=True, required=False, help="By default the files are stored in SQL format for sql databses and JSON format for NOSQL databases, Enable this flag to backup the databse files into csv format.")(func)
    return func

def check_parameters(auto_backup, interval, frequency, notification, slack_token, channel_id, restore, backup_file):
    errors = []

    # Check for auto_backup related conditions
    if auto_backup:
        if not (interval and frequency):
            errors.append(f"\n{RED}Error:- To enable auto backup, both --interval and --frequency must be provided.{RESET}")
    else:
        if interval or frequency:
            errors.append(f"\n{RED}Error:- Unexpected arguments: --interval or --frequency without --auto_backup.{RESET}")

    # Check for notification settings
    if notification:
        if not (slack_token and channel_id):
            errors.append(f"\n{RED}Error:- Both --slack_token and --channel_id must be provided for Slack notifications.{RESET}")
    else:
        if slack_token or channel_id:
            errors.append(f"\n{RED}Error:- Unexpected Slack arguments without --notification flag.{RESET}")

    # Check for restore conditions
    if restore:
        if not backup_file:
            errors.append(f"\n{RED}Error:- --backup_file is required for restoring backups.{RESET}")
    else:
        if backup_file:
            errors.append(f"\n{RED}Error:- Unexpected argument: --backup_file without --restore flag.{RESET}")

    # Check for mutually exclusive conditions (auto_backup and restore cannot be used together)
    if auto_backup and restore:
        errors.append(f"\n{RED}Error:- --auto_backup and --restore cannot be used together.{RESET}")

    # Display errors if there are any, or return True if all checks pass
    if not errors:
        return True
    else:
        for error in errors:
            click.echo(error)
        return False



@click.command()
@database_connection
@compress
@auto_backup
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_mysql(host, port, username, password,database_name, compress, auto_backup, interval, frequency,  notification, slack_token, channel_id, logging, restore, backup_dir, csv_backup_format, tables, backup_file):
    res = check_parameters(auto_backup, interval, frequency, notification, slack_token, channel_id, restore, backup_file)
    if res:
        from backup__mysql import backupmysql
        backupmysql(host, port, username, password, database_name, compress, notification, slack_token, channel_id, logging,restore, backup_dir, csv_backup_format, tables, backup_file)
        if auto_backup:
            from auto_backup_services import automatic_backup_process
            automatic_backup_process(host, port, username, password, database_name, compress, interval, frequency, notification, slack_token, channel_id, logging,restore, csv_backup_format, tables, backup_file, "SQL", "backup-mysql")


@click.command()
@database_connection
@compress
@auto_backup
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_postgresql(host, port, username, password,database_name, compress, auto_backup, interval, frequency, notification, slack_token, channel_id, logging, restore, backup_dir, csv_backup_format, tables, backup_file):
    from backup__postgresql import backuppostgresql
    res = check_parameters(auto_backup, interval, frequency, notification, slack_token, channel_id, restore, backup_file)
    if res:
        backuppostgresql(host, port, username, password, database_name, compress, notification, slack_token, channel_id, logging,restore, backup_dir, csv_backup_format, tables, backup_file)
        if auto_backup:
            from auto_backup_services import automatic_backup_process
            automatic_backup_process(host, port, username, password, database_name, compress, interval, frequency, notification, slack_token, channel_id, logging,restore, csv_backup_format, tables, backup_file, "SQL", "backup-postgresql")


@click.command()
@click.option("--database_name", "-db_name", required=True, help="Name of the database you want to backup")
@compress
@auto_backup
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_sqlite3(database_name, compress, auto_backup, interval, frequency, notification, slack_token, channel_id, logging, restore, backup_dir, csv_backup_format, tables, backup_file):
    from backup__sqlite3 import backupsqlite3
    res = check_parameters(auto_backup, interval, frequency, notification, slack_token, channel_id, restore, backup_file)
    if res:
        backupsqlite3(database_name, compress, notification, slack_token, channel_id, logging,restore, backup_dir, csv_backup_format, tables, backup_file)
        if auto_backup:
            from auto_backup_services import automatic_backup_process
            automatic_backup_process(None, None, None, None, database_name, compress, interval, frequency, notification, slack_token, channel_id, logging,restore, csv_backup_format, tables, backup_file, "SQL", "backup-sqlite3")


@click.command()
@database_connection
@compress
@auto_backup
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_sqlserver(host, port, username, password,database_name, compress, auto_backup, interval, frequency, notification, slack_token, channel_id, logging, restore, backup_dir, csv_backup_format, tables, backup_file):
    from backup__sqlserver import backupsqlserver
    res = check_parameters(auto_backup, interval, frequency, notification, slack_token, channel_id, restore, backup_file)
    if res:
        backupsqlserver(host, port, username, password, database_name, compress, notification, slack_token, channel_id, logging,restore, backup_dir, csv_backup_format, tables, backup_file)
        if auto_backup:
            from auto_backup_services import automatic_backup_process
            automatic_backup_process(host, port, username, password, database_name, compress, interval, frequency, notification, slack_token, channel_id, logging,restore, csv_backup_format, tables, backup_file, "SQL", "backup-sqlserver")


@click.command()
@database_connection
@compress
@auto_backup
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_mariadb(host, port, username, password,database_name, compress, auto_backup, interval, frequency, notification, slack_token, channel_id, logging, restore, backup_dir, csv_backup_format, tables, backup_file):
    from backup__mariadb import backupmariadb
    res = check_parameters(auto_backup, interval, frequency, notification, slack_token, channel_id, restore, backup_file)
    if res:
        backupmariadb(host, port, username, password, database_name, compress, notification, slack_token, channel_id, logging,restore, backup_dir, csv_backup_format, tables, backup_file)
        if auto_backup:
            from auto_backup_services import automatic_backup_process
            automatic_backup_process(host, port, username, password, database_name, compress, interval, frequency, notification, slack_token, channel_id, logging,restore, csv_backup_format, tables, backup_file, "SQL", "backup-mariadb")


@click.command()
@database_connection
@compress
@auto_backup
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@tables_option
def backup_oracledb(host, port, username, password,database_name, compress, auto_backup, interval, frequency, notification, slack_token, channel_id, logging, restore, backup_dir, csv_backup_format, tables, backup_file):
    from backup__oracledb import backuporacledb
    res = check_parameters(auto_backup, interval, frequency, notification, slack_token, channel_id, restore, backup_file)
    if res:
        backuporacledb(host, port, username, password, database_name, compress, notification, slack_token, channel_id, logging,restore, backup_dir, csv_backup_format, tables, backup_file)
        if auto_backup:
            from auto_backup_services import automatic_backup_process
            automatic_backup_process(host, port, username, password, database_name, compress, interval, frequency, notification, slack_token, channel_id, logging,restore, csv_backup_format, tables, backup_file, "SQL", "backup-oracledb")


@click.command()
@database_connection
@compress
@auto_backup
@notification
@logging_option
@restore_database
@backup_dir
@backup_format
@click.option("--collection_name","-col", multiple=True, required=False, help="Specify collections to back up. Use multiple '-col collection_name1 -col collection_name2 etc' for multiple collections.")
def backup_mongodb(host, port, username, password,database_name, compress, auto_backup, interval, frequency, notification, slack_token, channel_id, logging, restore, backup_dir, csv_backup_format, collection_name, backup_file):
    from backup__mongodb import backupmongodb
    res = check_parameters(auto_backup, interval, frequency, notification, slack_token, channel_id, restore, backup_file)
    if res:
        backupmongodb(host, port, username, password, database_name, compress, notification, slack_token, channel_id, logging, restore, backup_dir, csv_backup_format, collection_name, backup_file)
        if auto_backup:
            from auto_backup_services import automatic_backup_process
            automatic_backup_process(host, port, username, password, database_name, compress, interval, frequency, notification, slack_token, channel_id, logging, restore, csv_backup_format, collection_name, backup_file, "NOSQL", "backup-mongodb")


cli.add_command(backup_mysql)
cli.add_command(backup_postgresql)
cli.add_command(backup_sqlite3)
cli.add_command(backup_sqlserver)
cli.add_command(backup_oracledb)
cli.add_command(backup_mariadb)
cli.add_command(backup_mongodb)

if __name__ == "__main__":
    cli()