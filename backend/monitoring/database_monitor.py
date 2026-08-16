import psutil


# ------------------------------------------------------------
# Known database services
# ------------------------------------------------------------

DATABASES = {
    "MySQL": {
        "processes": ["mysqld.exe", "mysqld", "mariadbd.exe", "mariadbd"],
        "ports": [3306]
    },
    "PostgreSQL": {
        "processes": ["postgres.exe", "postgres"],
        "ports": [5432]
    },
    "MongoDB": {
        "processes": ["mongod.exe", "mongod"],
        "ports": [27017]
    },
    "Redis": {
        "processes": ["redis-server.exe", "redis-server"],
        "ports": [6379]
    },
    "Microsoft SQL Server": {
        "processes": ["sqlservr.exe", "sqlservr"],
        "ports": [1433]
    },
    "Oracle": {
        "processes": ["oracle.exe", "oracle"],
        "ports": [1521]
    }
}


# ------------------------------------------------------------
# Get listening ports
# ------------------------------------------------------------

def get_listening_ports():

    ports = set()

    try:

        connections = psutil.net_connections(kind="inet")

        for connection in connections:

            if connection.status == psutil.CONN_LISTEN:

                if connection.laddr:

                    ports.add(connection.laddr.port)

    except Exception:
        pass

    return ports


# ------------------------------------------------------------
# Get running process names
# ------------------------------------------------------------

def get_running_processes():

    processes = set()

    try:

        for process in psutil.process_iter(["name"]):

            try:

                name = process.info["name"]

                if name:
                    processes.add(name.lower())

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    except Exception:
        pass

    return processes


# ------------------------------------------------------------
# Detect databases
# ------------------------------------------------------------

def get_database_status():

    listening_ports = get_listening_ports()
    running_processes = get_running_processes()

    databases = []

    for database, config in DATABASES.items():

        process_found = any(
            process.lower() in running_processes
            for process in config["processes"]
        )

        port_found = any(
            port in listening_ports
            for port in config["ports"]
        )

        if process_found or port_found:

            detected_port = next(
                (
                    port
                    for port in config["ports"]
                    if port in listening_ports
                ),
                config["ports"][0]
            )

            databases.append({
                "service": database,
                "host": "localhost",
                "port": detected_port,
                "status": "Running",
                "version": "-",
                "threads_connected": "-",
                "threads_running": "-"
            })

    return databases