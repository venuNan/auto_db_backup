import os
import datetime
import csv
import gzip
import shutil

def sql_backup(csv_backup_format, compress, backup_dir, total_tables, database_name, cursor, notification, slack_token, channel_id, log) -> None:
    # Create the main backup directory
    backup_dir = os.path.join(backup_dir, "Database_backup_files")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Create a folder for the specific database
    database_backup_dir = os.path.join(backup_dir, f"{database_name}-database")
    if not os.path.exists(database_backup_dir):
        os.makedirs(database_backup_dir)

    for table_name in total_tables:
        # Create a timestamped backup file
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M')
        if csv_backup_format:
            backup_file = os.path.join(database_backup_dir, f"{table_name}_{timestamp}.csv")
        else:
            backup_file = os.path.join(database_backup_dir, f"{table_name}_{timestamp}.sql")

        try:
            if csv_backup_format:
                with open(backup_file, 'w', newline='') as f:
                    # Fetch table data
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    
                    # Write CSV file with headers
                    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                    columns = [column[0] for column in cursor.fetchall()]
                    
                    writer = csv.writer(f)
                    writer.writerow(columns)  # Write column headers
                    writer.writerows(rows)    # Write table rows

            else:
                # If not CSV, create SQL format
                with open(backup_file, 'w') as f:
                    # Write SQL format
                    cursor.execute(f"SHOW CREATE TABLE {table_name}")
                    create_table_stmt = cursor.fetchone()[1]
                    f.write(f"-- Table structure for `{table_name}`\n")
                    f.write(f"{create_table_stmt};\n\n")
                    
                    # Fetch table data
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()

                    # Write the INSERT statements
                    if rows:
                        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                        columns = [column[0] for column in cursor.fetchall()]
                        columns_str = ', '.join([f"`{col}`" for col in columns])

                        f.write(f"-- Dumping data for table `{table_name}`\n")
                        f.write(f"INSERT INTO `{table_name}` ({columns_str}) VALUES\n")
                        
                        for idx, row in enumerate(rows):
                            values_str = ', '.join([f"'{str(value)}'" if value is not None else 'NULL' for value in row])
                            if idx == len(rows) - 1:
                                f.write(f"({values_str});\n")  # Last row ends with a semicolon
                            else:
                                f.write(f"({values_str}),\n")  # Other rows end with a comma
                    else:
                        f.write(f"-- No data for table `{table_name}`\n\n")

            # Compress SQL file if compress flag is set
            if compress :
                with open(backup_file, 'rb') as f_in:
                    with gzip.open(f"{backup_file}.gz", 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(backup_file)  # Remove uncompressed file after compressing

        except Exception as e:
            log.error(f"Error backing up table {table_name}: {e}")

    # Notify if needed (this part is placeholder for real notification handling)
    if notification:
        print(f"Notification sent to Slack channel {channel_id} (dummy)")
