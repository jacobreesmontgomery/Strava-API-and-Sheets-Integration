console.log("Data: ", headers)

function filterTable(columnName) {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("filter" + columnName);
    filter = input.value.toUpperCase();
    table = document.getElementById("dataTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[getIndex(columnName)];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function getIndex(columnName) {
    var headers = document.getElementById("dataTable").getElementsByTagName("th");
    for (var i = 0; i < headers.length; i++) {
        if (headers[i].textContent === columnName) {
            return i;
        }
    }
    return -1; // If column name not found
}

// Add a filter for each column
for (header in headers) {
    filterTable(header);
}