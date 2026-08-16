async function refreshDatabases() {

    try {

        const response = await fetch("/api/database");

        if (!response.ok) {
            throw new Error("Failed to fetch database information");
        }

        const databases = await response.json();

        const table = document.getElementById("databaseTable");

        const databaseCount =
            document.getElementById("databaseCount");

        const runningCount =
            document.getElementById("runningCount");

        const offlineCount =
            document.getElementById("offlineCount");


        // --------------------------------------------------
        // Update counts
        // --------------------------------------------------

        const running = databases.filter(
            database => database.status === "Running"
        ).length;

        const offline = databases.filter(
            database => database.status !== "Running"
        ).length;


        databaseCount.innerText = databases.length;

        runningCount.innerText = running;

        offlineCount.innerText = offline;


        // --------------------------------------------------
        // No databases detected
        // --------------------------------------------------

        if (databases.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="5"
                        class="text-center text-muted py-4">

                        <i class="bi bi-database-x"></i>

                        No Database Services Detected

                    </td>
                </tr>
            `;

            return;
        }


        // --------------------------------------------------
        // Build table
        // --------------------------------------------------

        let rows = "";

        databases.forEach(database => {

            const statusClass =
                database.status === "Running"
                    ? "bg-success"
                    : "bg-danger";


            rows += `
                <tr>

                    <td>
                        <i class="bi bi-database"></i>
                        ${database.service}
                    </td>

                    <td>
                        ${database.host}
                    </td>

                    <td>
                        ${database.port}
                    </td>

                    <td>
                        <span class="badge ${statusClass}">
                            ${database.status}
                        </span>
                    </td>

                    <td>
                        ${database.version}
                    </td>

                </tr>
            `;

        });


        table.innerHTML = rows;

    }

    catch (error) {

        console.error(
            "Database monitoring error:",
            error
        );

    }

}


// Initial load
refreshDatabases();


// Refresh every 5 seconds
setInterval(refreshDatabases, 5000);