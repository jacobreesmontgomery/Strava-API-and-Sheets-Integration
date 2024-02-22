document.addEventListener('DOMContentLoaded', function() {
    var headerStats = document.getElementById("header-stats").getAttribute("data-argument");
    headerStats = headerStats.slice(1, -1).split(",");
    headerStats = headerStats.map(function(item) {
        return item.trim().slice(1, -1);
    });
    console.log("Headers: ", headerStats);

    var recapData = document.getElementById("recap-data").getAttribute("data-argument");
    recapData = recapData.slice(1, -1).split(",");
    recapData = recapData.map(function(item) {
        if (item != "" || item) {
            return item.replace(/[\[\]']/g, '').trim();
        } else {
            return null; // Make empty elements as null
        }
    }).filter(item => item != "" && item);

    NUM_ATHLETES = 6;
    NUM_HEADERS = 13;
    var arr = new Array(NUM_ATHLETES);
    for (var i = 0; i < arr.length; i++) {
        arr[i] = new Array(NUM_HEADERS);
    }
    // 5 is the number of athletes
    counter = 0;
    for (var i = 0; i < arr.length; i++) {
        for (var j = 0; j < arr[i].length; j++) {
            arr[i][j] = recapData[counter];
            counter++;
        }
    }
    recapData = arr; // Overwriting recapData with the populated 2D array
    console.log("Recap data: ", recapData);

    // Populate table with initial data
    populateTable(headerStats, recapData);

    // Attach event listener to input for filtering
    // document.getElementById('searchInput').addEventListener('keyup', filterTable);
});

/**
 *  Populates the table with its headers and recap data.
 * */ 
function populateTable(headerStats, recapData) {
    const tableHeader = document.querySelector('#dataTable thead');
    tableHeader.innerHTML = '';

    const row = document.createElement('tr');
    headerStats.forEach(header => {
        const cell = document.createElement('th');
        // Might have to do sumn here to make these headers filterable
        cell.textContent = header;
        row.appendChild(cell);
    });
    tableHeader.appendChild(row);

    const tableBody = document.querySelector('#dataTable tbody');
    tableBody.innerHTML = '';

    recapData.forEach(item => {
        const row = document.createElement('tr');
        Object.values(item).forEach(value => {
            const cell = document.createElement('td');
            cell.textContent = value;
            row.appendChild(cell);
        });
        tableBody.appendChild(row);
    });
}

/**
 * Filters the table based on the input value.
 * */
function filterTable() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toUpperCase();
    const table = document.getElementById('dataTable');
    const rows = table.getElementsByTagName('tr');

    for (let i = 0; i < rows.length; i++) {
        let shouldDisplay = false;
        const cells = rows[i].getElementsByTagName('td');
        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            if (cell) {
                const textValue = cell.textContent || cell.innerText;
                if (textValue.toUpperCase().indexOf(filter) > -1) {
                    shouldDisplay = true;
                    break;
                }
            }
        }
        rows[i].style.display = shouldDisplay ? '' : 'none';
    }
}