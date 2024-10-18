import pyodbc

def backupsqlserver(host:str, username:str, passwd, database_name:str, compress:bool, storage_option: str, logging:bool, port_no:int=1433) -> None:
    # Connect to the SQL Server database
    connection = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=server_name;'
        'DATABASE=your_database;'
        'UID=username;'
        'PWD=password'
    )
    cursor = connection.cursor()

    # Execute a SELECT query
    cursor.execute("SELECT * FROM your_table WHERE id = ?", (1,))
    result = cursor.fetchall()

    # Commit if needed
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()