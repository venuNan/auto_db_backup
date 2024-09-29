import os
import datetime


def cloud_backup() -> None:
    pass


def local_backup(csv_backup_format, backup_dir, total_tables, database_name, cursor) -> None:

    backup_dir = './Dtabase_backup_files'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Create a timestamped backup file
    # Open the backup file for writing
    for table_name in total_tables:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f"{database_name}_{table_name}_{timestamp}.sql")

        with open(backup_file, 'w') as f:
            # Get the CREATE TABLE statement
            cursor.execute(f"SHOW CREATE TABLE {table_name}")
            create_table_stmt = cursor.fetchone()[1]
            f.write(f"-- Table structure for `{table_name}`\n")
            f.write(f"{create_table_stmt};\n\n")
            
            # Fetch the table data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Write the INSERT statements
            if rows:
                columns_query = f"SHOW COLUMNS FROM {table_name}"
                cursor.execute(columns_query)
                columns = [column[0] for column in cursor.fetchall()]
                columns_str = ', '.join([f"`{col}`" for col in columns])
                f.write(f"-- Dumping data for table `{table_name}`\n")
                f.write(f"INSERT INTO `{table_name}` ({columns_str}) VALUES\n")
                
                # Loop through the rows
                for idx, row in enumerate(rows):
                    values_str = ', '.join([f"'{str(value)}'" if value is not None else 'NULL' for value in row])
                    if idx == len(rows) - 1:
                        f.write(f"({values_str});\n")  # Last row ends with a semicolon
                    else:
                        f.write(f"({values_str}),\n")  # Other rows end with a comma
            else:
                f.write(f"-- No data for table `{table_name}`\n\n")


