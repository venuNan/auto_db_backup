import click
import db_backup
import os

APP_VERSION = "1.0"

@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show the version of the app and exit')
def cli(version):
    if version:
        click.echo(f"Auto_db_backup   {APP_VERSION}")

def common_options(func):
    func = click.option("--storage_option", "-so", required=True, type=click.Choice(["local", "cloud"]), help="Where to store the backup, in the cloud or local system")(func)
    func = click.option("--compress", "-c", is_flag=True, help="Store the files in a compressed format like gzip or tar")(func)
    func = click.option("--logging", "-log", is_flag=True, help="Log the operations performed on the database and the timing of the backup")(func)
    func = click.option("--auto_backup", "-ab", is_flag=True, default=False, help="Automate the backup process")(func)
    func = click.option('--backup_dir', default=f'{os.getcwd()}', hidden=True)(func)
    func = click.option("--passwd", "-pw", required=True, help="Password of the database")(func)
    func = click.option("--database_name", "-db_name", required=True, help="Name of the database you want to backup")(func)
    func = click.option("--username", "-u", required=True, help="Username of the database")(func)
    func = click.option("--port", "-p", required=True, help="Port number of the database")(func)
    func = click.option("--host", "-h", required=True, help="The IP address of the database")(func)
    return func

def tables_option(func):
    func = click.option("--tables", "-t", multiple=True, required=False, help="Specify tables to back up. Use multiple '-t table_name' for multiple tables.")(func)
    return func

def auto_backup():
       pass

@click.command()
@common_options
@tables_option
def backup_mysql(host, port, username, passwd,database_name, tables, compress, storage_option, logging, auto_backup, backup_dir):
        db_backup.backup_mysql(
            host, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir, port_no=port
        )
        if auto_backup:
            print("auto backup intialised")
@click.command()
@common_options
@tables_option
def backup_postgresql(host, port, username, passwd,database_name, tables, compress, storage_option, logging, auto_backup, backup_dir):
        db_backup.backup_postgresql(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

@click.command()
@common_options
@tables_option
def backup_sqlite3(host, port, username, passwd,database_name, tables, compress, storage_option, logging, auto_backup, backup_dir):
        db_backup.backup_sqlite3(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

@click.command()
@common_options
@tables_option
def backup_sqlserver(host, port, username, passwd,database_name, tables, compress, storage_option, logging, auto_backup, backup_dir):
        db_backup.backup_sqlserver(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

@click.command()
@common_options
@tables_option
def backup_mariadb(host, port, username, passwd,database_name, tables, compress, storage_option, logging, auto_backup, backup_dir):
        db_backup.backup_mariadb(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

@click.command()
@common_options
@tables_option
def backup_oracledb(host, port, username, passwd,database_name, tables, compress, storage_option, logging, auto_backup, backup_dir):
        db_backup.backup_oracledb(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

@click.command()
@common_options
@tables_option
def backup_sybase(host, port, username, passwd,database_name, tables, compress, storage_option, logging, auto_backup, backup_dir):
        db_backup.backup_sybase(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

@click.command()
@common_options
@tables_option
def backup_teradata(host, port, username, passwd,database_name, tables, compress, storage_option, logging, auto_backup, backup_dir):
        db_backup.backup_teradata(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

@click.command()
@common_options
@click.option("--collection_name","-col", multiple=True, required=False, help="Specify collections to back up. Use multiple '-col collection_name' for multiple collections.")
def backup_mongodb(host, port, username, passwd,database_name, collection_name, compress, storage_option, logging, auto_backup, backup_dir):
        db_backup.backup_mongodb(
            host, port, username, passwd, database_name, collection_name, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

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