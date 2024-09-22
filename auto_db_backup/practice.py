# def autobackup(database, host, username, passwd, database_name, tables, compress, storage_option, logging, backup_dir, port) -> None:
#     cmd = [
#     "auto_db_backup",database , "-h", host, "-p", str(port), "-u", username,
#     "-pw", passwd, "-db_name", database_name
#     ]

#     # Add compression option if enabled
#     if compress:
#         cmd.append("-c")

#     # Add storage option
#     cmd.extend(["-so", storage_option])

#     # Add logging option if enabled
#     if logging:

#         cmd.append("-log")

#     # Add backup directory option if provided
#     if backup_dir:
#         cmd.extend(["--backup_dir", backup_dir])

#     # Loop through the tables and add each table to the comman
#     for table in tables:
#         cmd = cmd + ["-t", table]

#     subprocess.run(cmd)



import os

# Set an environment variable
os.environ['MY_VARIABLE'] = 'my_value'

# Get the environment variable
print(os.getenv('MY_VARIABLE'))  # Output: my_value
