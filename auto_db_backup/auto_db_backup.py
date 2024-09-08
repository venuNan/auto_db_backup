import click



@click.group()
def cli() -> None:
    pass

@click.command()
@click.option("--database","-db",
              type=click.Choice(["mysql", "postgresql","sqlite3","sqlserver","mariadb","oracledb","sybase","teradata"]),
              required=True ,
              help="Types of databse EX:- MYSQL, postgresql, SQLServer, SQlite3, tec.")
@click.option("--host" ,"-h" ,
              required=True,
                help="the addrees of the database")
@click.option("--port","-p",required=True,help="port numbers of the databse")
def backup(database,host,port):
    print("db type of",database, host, port)






cli.add_command(backup)

if __name__ == "__main__":
    cli()