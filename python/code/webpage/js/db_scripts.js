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

    NUM_HEADERS = headerStats.length;
    NUM_ATHLETES = recapData.length / NUM_HEADERS;
    var arr = new Array(NUM_ATHLETES);
    for (var i = 0; i < arr.length; i++) {
        arr[i] = new Array(NUM_HEADERS);
    }
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

    // Setting up columns to be sortable
    createSortableColumns();
});

/**
 *  Populates the table with its headers and recap data.
 * */ 
function populateTable(headerStats, recapData) {
    const tableHeader = document.querySelector('#dataTable thead');
    tableHeader.innerHTML = '';

    // Initial header row
    const row = document.createElement('tr');
    var counter = 0;
    headerStats.forEach(header => {
        const cell = document.createElement('th');
        // cell.textContent = header;
        const col = document.createElement('p');
        col.textContent = header;
        col.className = 'headerCols';
        cell.appendChild(col);
        row.appendChild(cell);

        // Create the input element
        const input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('id', header + 'Input');
        input.setAttribute('placeholder', 'Search by ' + header + '...');
        input.setAttribute('onkeyup', 'filterHeader(' + counter + ')');

        // Append input to a header element
        cell.appendChild(input);
        counter++;
    });
    tableHeader.appendChild(row);

    // Data cells
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
 * Establishes a filter for the incoming header.
 * @param {*} header 
 */
function filterHeader(columnIndex) {
    var input, filter, table, tr, td, i;
    input = document.getElementById("dataTable").getElementsByTagName("input")[columnIndex];
    filter = input.value.toUpperCase();
    table = document.getElementById("dataTable");
    tr = table.getElementsByTagName("tr");
    // Skipping first row (headers with filters)
    for (i = 1; i < tr.length; i++) {
        var matchFound = false;
        td = tr[i].getElementsByTagName("td")[columnIndex];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                matchFound = true;
            }
        }
        if (matchFound) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}

function createSortableColumns() {
    const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;
    
    const comparer = (idx, asc) => (a, b) => ((v1, v2) =>
        v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));
    
    document.querySelectorAll('th').forEach(th => th.addEventListener('click', () => {
        const table = th.closest('table');
        const tbody = table.querySelector('tbody');
        Array.from(tbody.querySelectorAll('tr'))
            .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
            .forEach(tr => tbody.appendChild(tr));
    }));
}