import pytest
from click.testing import CliRunner
import auto_db_backup.main as main

@pytest.fixture
def runner():
    return CliRunner()


def test_version_option(runner):
    result = runner.invoke(main.cli, ['--version'])
    assert result.exit_code == 0
    assert "Auto_db_backup" in result.output


def test_mysql_backup_with_missing_params(runner):
    result = runner.invoke(main.backup_mysql, [
        '--host', 'localhost',
        '--port', '3306',
        '--username', 'root',
        '--passwd', 'password',
        '--database_name', 'testdb'
    ])
    assert result.exit_code == 1
    assert "Error" not in result.output


def test_mysql_backup_with_auto_backup(runner):
    result = runner.invoke(main.backup_mysql, [
        '--host', 'localhost',
        '--port', '3306',
        '--username', 'root',
        '--passwd', 'password',
        '--database_name', 'testdb',
        '--auto_backup',
        '--interval', '2',
        '--frequency', 'minutes'
    ])
    assert result.exit_code == 0
    assert "Error" not in result.output


def test_postgresql_backup_with_cloud_option(runner):
    result = runner.invoke(main.backup_postgresql, [
        '--host', 'localhost',
        '--port', '5432',
        '--username', 'postgres',
        '--passwd', 'password',
        '--database_name', 'testdb',
        '--storage_option',
        '--provider', 'aws'
    ])
    assert result.exit_code == 0
    assert "Error" not in result.output


def test_mongodb_backup_with_collection_option(runner):
    result = runner.invoke(main.backup_mongodb, [
        '--host', 'localhost',
        '--port', '27017',
        '--username', 'admin',
        '--passwd', 'password',
        '--database_name', 'testdb',
        '--collection_name', 'users',
        '--collection_name', 'orders'
    ])
    assert result.exit_code == 0
    assert "Error" not in result.output


def test_restore_option(runner):
    result = runner.invoke(main.backup_mysql, [
        '--host', 'localhost',
        '--port', '3306',
        '--username', 'root',
        '--passwd', 'password',
        '--database_name', 'testdb',
        '--restore',
        '--backup_file', 'backup.sql'
    ])
    assert result.exit_code == 0
    assert "Backup file path is not provided" not in result.output

