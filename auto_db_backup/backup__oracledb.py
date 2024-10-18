
import cx_Oracle



def backuporacledb(host:str, username:str, passwd, database_name:str, compress:bool, storage_option: str, logging:bool, port_no:int=1521) -> None:

    # Connect to the Oracle database
    connection = cx_Oracle.connect(
        user=username,
        password=passwd,
        dsn="localhost/orcl"
    )
    cursor = connection.cursor()

    # Execute a SELECT query
    cursor.execute("SELECT * FROM your_table WHERE id = :id", id=1)
    result = cursor.fetchall()

    # Commit if necessary
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

