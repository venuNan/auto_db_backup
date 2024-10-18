import psycopg2

def backuppostgresql(host:str, username:str, passwd:str, database_name:str, compress:bool, storage_option: str, logging:bool, port_no:int=5432) -> None:
    

    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host="localhost",
        user="username",
        password="password",
        dbname="your_database"
    )
    cursor = connection.cursor()

    # Execute a SELECT statement
    cursor.execute("SELECT * FROM your_table WHERE id = %s", (1,))
    result = cursor.fetchall()

    # Commit any changes if necessary
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()


