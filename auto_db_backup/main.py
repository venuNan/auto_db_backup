import click
import db_backup
import os

APP_VERSION = "1.0"

@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show the version of the app and exit')
def cli(version):
    if version:
        click.echo(f"Auto_db_backup   {APP_VERSION}")

@click.command()
@click.option("--database","-db",
              type=click.Choice(["mysql", "postgresql","sqlite3","sqlserver","mariadb","oracledb","sybase","teradata"]),
              required=True ,
              help="Type of databse EX:- MYSQL, postgresql, SQLServer, SQlite3, tec.")
@click.option("--host", "-h", required=True, help="The ip addrees of the database")
@click.option("--port", "-p", required=True, help="Port number of the databse")
@click.option("--username", "-u", required=True, help="Username of the database")
@click.option("--database_name", "-db_name", required=True, help="Name of the database you want to backup")
@click.option("--passwd", "-pw", required=True, help="Password of the database")
@click.option("--tables", "-t", multiple=True, required=False, help="If you want to backup certain tables in the databse.\n If you want to add multiple tables enter like '-t table_name1 -t table_name2'")
@click.option("--compress", "-c", is_flag=True, help="To store the files in a compressed format like gzip and tar files")
@click.option("--storage_option", "-so", required=True, type=click.Choice(["local","cloud"]), help="Where to store the backup in the cloud or local system")
@click.option("--logging", "-log", is_flag=True, help="To log the operation perfomed on the databse and the timing of the backup")
@click.option("--auto_backup", "-ab", is_flag=True, default="no",help="To the automate the backup process")
@click.option('--backup_dir', default=f'{os.getcwd()}', hidden=True)
def backup(database, host, port, username, passwd,database_name, tables, compress, storage_option, logging, auto_backup, backup_dir):

    if database=="mysql":
        db_backup.backup_mysql(host, username, passwd, database_name, tables, compress, storage_option, logging, auto_backup, backup_dir, port_no=port )

    if database == "mysql":
        db_backup.backup_mysql(
            host, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir, port_no=port
        )

    elif database == "postgresql":
        db_backup.backup_postgresql(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

    elif database == "sqlite3":
        db_backup.backup_sqlite3(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

    elif database == "sqlserver":
        db_backup.backup_sqlserver(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

    elif database == "mariadb":
        db_backup.backup_mariadb(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

    elif database == "oracledb":
        db_backup.backup_oracledb(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

    elif database == "sybase":
        db_backup.backup_sybase(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

    elif database == "teradata":
        db_backup.backup_teradata(
            host, port, username, passwd, database_name, tables, compress, storage_option, 
            logging, auto_backup, backup_dir
        )

    else:
        click.echo(f"Unsupported database: {database}")


cli.add_command(backup)
if __name__ == "__main__":
    cli()