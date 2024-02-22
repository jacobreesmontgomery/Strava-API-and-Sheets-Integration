var headerStats = document.getElementById("headerStats").getAttribute("data-argument");
console.log("Header stats:", headerStats);

var recapData = document.getElementById("recapData").getAttribute("data-argument");
console.log("Recap data:", recapData);

// // Function to populate table with data
// function populateTable(data) {
//     const tableBody = document.querySelector('#dataTable tbody');
//     tableBody.innerHTML = '';

//     data.forEach(item => {
//         const row = document.createElement('tr');
//         Object.values(item).forEach(value => {
//             const cell = document.createElement('td');
//             cell.textContent = value;
//             row.appendChild(cell);
//         });
//         tableBody.appendChild(row);
//     });
// }

// // Function to filter table based on input value
// function filterTable() {
//     const input = document.getElementById('searchInput');
//     const filter = input.value.toUpperCase();
//     const table = document.getElementById('dataTable');
//     const rows = table.getElementsByTagName('tr');

//     for (let i = 0; i < rows.length; i++) {
//         let shouldDisplay = false;
//         const cells = rows[i].getElementsByTagName('td');
//         for (let j = 0; j < cells.length; j++) {
//             const cell = cells[j];
//             if (cell) {
//                 const textValue = cell.textContent || cell.innerText;
//                 if (textValue.toUpperCase().indexOf(filter) > -1) {
//                     shouldDisplay = true;
//                     break;
//                 }
//             }
//         }
//         rows[i].style.display = shouldDisplay ? '' : 'none';
//     }
// }

// // Populate table with initial data
// populateTable(data);

// // Attach event listener to input for filtering
// document.getElementById('searchInput').addEventListener('keyup', filterTable);
