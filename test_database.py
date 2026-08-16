from backend.monitoring.database_monitor import get_database_status


databases = get_database_status()


if not databases:

    print("No database services detected.")

else:

    for database in databases:

        print(database)