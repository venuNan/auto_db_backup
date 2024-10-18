try:
    backup_file_path = "C:\Users\Venu\Database_backup_files\user-databse\customers_2024:10:17_17:12:42.sql"
    # your backup logic here
    with open(backup_file_path, "w") as f:
        f.write("Backup data")
except Exception as e:
    print(f"Failed to create backup: {str(e)}")