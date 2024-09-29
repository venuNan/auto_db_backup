import subprocess
import click
import logging
import schedule
import time

# ANSI escape codes for colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s", )

def backup_process(host, port, username, passwd, database_name, compress, storage_option, provider, notification, slack_token, channel_id, log, restore, csv_backup_format, tables, backup_file, databse_type, rdbms):
    cmd = ["python","main.py", rdbms, "-h", host, "-p", port, "-u", username, "-pw", passwd, "-db_name", database_name]
    if compress:
        cmd.append("-c")
    if storage_option:
        cmd.extend(["-so", "-prov", provider])
    if notification:
        cmd.extend(["-n", "-st", slack_token, "-ct", channel_id])
    if logging:
        cmd.append("-log")
    if restore:
        cmd.extend(["-r","--backup_file", backup_file])
    if csv_backup_format:
        cmd.append("-cf")
    if tables and databse_type=="SQL":
        for table in tables:
            cmd.extend["-t",table]
    else:
        for collection in tables:
            cmd.extend(["-col", collection])
    result = subprocess.run(cmd,shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        click.echo("Subprocess executed successfully!")
        click.echo(" - ".join(cmd))
    else:
        click.echo(f"Subprocess failed with return code {result.returncode}")

    

def automatic_backup_process(host, port, username, passwd, database_name, compress, interval, frequency, storage_option, provider, notification, slack_token, channel_id, log, restore, csv_backup_format, tables, backup_file, database_type, rdbms):
    def autobackup():
        try:
            backup_process(host, port, username, passwd, database_name, compress, storage_option, provider, notification, slack_token, channel_id, log, restore, csv_backup_format, tables, backup_file, database_type, rdbms)
            logging.info(f"{GREEN}Backup process completed successfully!{RESET}")
        except Exception as e:
            logging.error(f"{RED}Error during the backup process: {str(e)}{RESET}")
            

    if frequency == "seconds":
        schedule.every(int(interval)).seconds.do(autobackup)
    elif frequency == "minutes":
        schedule.every(int(interval)).minutes.do(autobackup)
    elif frequency == "hours":
        schedule.every(int(interval)).hours.do(autobackup)
    else:
        schedule.every(int(interval)).days.do(autobackup)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info(f"{RED}Backup automation stopped by the user.{RESET}")