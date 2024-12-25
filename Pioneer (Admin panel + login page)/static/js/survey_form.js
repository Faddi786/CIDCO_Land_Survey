document.addEventListener("DOMContentLoaded", function () {
    const nodeInput = document.getElementById("node_name");
    const sectorInput = document.getElementById("sector_no");
    const blockInput = document.getElementById("block_name");
    const plotInput = document.getElementById("plot_name");
 
    // Store the autocomplete data for validation

    let autocompleteData = {
        Node_Name: [],
        Sector: [],
        Block_Name: [],
        Plot_No: []
    };

    // Set initial states
    nodeInput.style.backgroundColor = "lightgrey";
    sectorInput.style.backgroundColor = "darkgrey";
    blockInput.style.backgroundColor = "darkgrey";
    plotInput.style.backgroundColor = "darkgrey";

    sectorInput.disabled = true;
    blockInput.disabled = true;
    plotInput.disabled = true;

    // Fetch initial data
    fetchDropdownData();

    // Autocomplete function 
    function autocomplete(inp, data, nextField) {
        let currentFocus;

        inp.addEventListener("input", function () {
            closeAllLists();
            const val = this.value;
            if (!val) return false;
            currentFocus = -1;

            const a = document.createElement("DIV");
            a.setAttribute("id", this.id + "autocomplete-list");
            a.setAttribute("class", "autocomplete-items");
            this.parentNode.appendChild(a);

            for (let i = 0; i < data.length; i++) {
                if (data[i].toUpperCase().includes(val.toUpperCase())) {
                    const b = document.createElement("DIV");
                    b.innerHTML = `<strong>${data[i].substr(0, val.length)}</strong>${data[i].substr(val.length)}`;
                    b.innerHTML += `<input type='hidden' value='${data[i]}'>`;

                    b.addEventListener("click", function () {
                        inp.value = this.getElementsByTagName("input")[0].value;
                        closeAllLists();

                        // Enable the next field and set its style
                        if (nextField) {
                            nextField.disabled = false;
                            nextField.style.backgroundColor = "lightgrey";
                            fetchDropdownData(getFiltersForField(nextField));
                        }
                        // Lock the current field after valid selection
                        inp.style.backgroundColor = "white";
                        inp.disabled = true;
                    });

                    a.appendChild(b);
                }
            }
        });

        function closeAllLists(elmnt) {
            const x = document.getElementsByClassName("autocomplete-items");
            for (let i = 0; i < x.length; i++) {
                if (elmnt != x[i] && elmnt != inp) x[i].parentNode.removeChild(x[i]);
            }
        }

        document.addEventListener("click", function (e) {
            closeAllLists(e.target);
        });
    }

    // Fetch dropdown data with filters
    function fetchDropdownData(filters = {}) {
        const params = new URLSearchParams(filters).toString();

        fetch(`/get_dropdown_values?${params}`)
            .then(response => response.json())
            .then(data => {
                if (!filters.node_name) {
                    autocompleteData.Node_Name = data.Node_Name || [];
                    autocomplete(nodeInput, autocompleteData.Node_Name, sectorInput);
                }
                if (filters.node_name && !filters.sector) {
                    autocompleteData.Sector = data.Sector || [];
                    autocomplete(sectorInput, autocompleteData.Sector, blockInput);
                }
                if (filters.sector && !filters.block_name) {
                    autocompleteData.Block_Name = data.Block_Name || [];
                    autocomplete(blockInput, autocompleteData.Block_Name, plotInput);
                }
                if (filters.block_name) {
                    autocompleteData.Plot_No = data.Plot_No || [];
                    autocomplete(plotInput, autocompleteData.Plot_No, null);
                }
            })
            .catch(err => console.error("Error fetching dropdown data:", err));
    }

    // Get filters based on the field
    function getFiltersForField(field) {
        if (field === sectorInput) return { node_name: nodeInput.value };
        if (field === blockInput) return { node_name: nodeInput.value, sector: sectorInput.value };
        if (field === plotInput) return { node_name: nodeInput.value, sector: sectorInput.value, block_name: blockInput.value };
        return {};
    }
});



    // Add an event listener to submit the form
document.getElementById("plotForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission
    submitFormData(); // Call the function to send the form data using XHR
});



function submitFormData() {
    // Create a new FormData object
    var formData = new FormData(document.getElementById("plotForm"));

    console.log("Form data before processing:");
    console.log([...formData.entries()]); // Log form data before adding defaults



// {}for owner

    // Process the Owner table data
    const ownerRows = document.querySelectorAll("#transferDetails table tr");
    let owners = [];

    // Skip the header row, process only the data rows
    for (let i = 1; i < ownerRows.length; i++) {
        const row = ownerRows[i];
        const ownerName = row.querySelector(`#t${i}owner_name`)?.value || '-';
        const transferDate = row.querySelector(`#t${i}transfer_date`)?.value || '-';

        // Format as name-date
        const ownerString = `${ownerName}|${transferDate}`;
        owners.push(ownerString);
    }

    console.log('Owner Details:', owners);

    // Convert the array to a comma-separated string or set a default "-"
    const ownerString = owners.length > 0 ? owners.join(", ") : "-";
    console.log('Formatted Owner String:', ownerString);



// {}for owner



    // Process the Area table data
    const rows = document.querySelectorAll("#areaDetails table tr");
    let area = [];

    // Skip the header row, process only the data rows
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const length = row.querySelector(`#length${i}`)?.value || 0;
        const width = row.querySelector(`#width${i}`)?.value || 0;
        const calculatedArea = row.querySelector(`#calculatedArea${i}`)?.innerText || 0;

        // Format as lxb=area
        const areaString = `${length}x${width}=${calculatedArea}`;
        area.push(areaString);
    }
    console.log('me yaha hu ');
    console.log(area);
    

    // Convert arrays to comma-separated strings or set default "-"
    const areaString = area.length > 0 ? area.join(", ") : "-";





    // Add these values to FormData
    formData.set("area", areaString);
    formData.set("ownerNtransferDate", ownerString)// {} write the loginc of formData.set here just like above

    console.log("Form data after processing area & owners table:");
    console.log([...formData.entries()]); // Log form data after processing area table

    // Create a new XMLHttpRequest object
    var xhr = new XMLHttpRequest();

    // Configure the request
    xhr.open("POST", "/submit_form_data", true);

    // Set up a callback to handle the response
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Handle successful form submission
            alert("Form submitted successfully!");
        } else {
            // Handle errors
            alert("Error submitting form: " + xhr.statusText);
        }
    };

    // Send the FormData with the XHR request
    xhr.send(formData);
}


// owner starts from here

let ownerCount = 2; // Start from 2 since you want t2 fields to be created first.

// Create the table structure initially
const transferDetails = document.getElementById("transferDetails");
const table = document.createElement("table");
table.setAttribute("border", "1");
table.style.width = "100%";

// Add table headers
const headerRow = document.createElement("tr");
headerRow.innerHTML = `
    <th>Owner</th>
    <th>Name</th>
    <th>Date</th>
    <th>Actions</th>    
`;
table.appendChild(headerRow);
transferDetails.appendChild(table);

const firstOwner = document.createElement("tr");

firstOwner.innerHTML = `
    <td>owner 1</td>
    <td><input type="text" id="t1owner_name" name="t1owner_name" placeholder="Enter Name" required></td>
    <td><input type="date" id="t1transfer_date" name="t1transfer_date" required></td>
    <td></td> <!-- No action button for the first row -->
`;
table.appendChild(firstOwner)
// Event listener to add a new owner row
document.getElementById("addOwner").addEventListener("click", () => {
    if (ownerCount <= 12) {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>Owner ${ownerCount}</td>
            <td>
                <input type="text" id="t${ownerCount}owner_name" name="t${ownerCount}owner_name" placeholder="Enter Name">
            </td>
            <td>
                <input type="date" id="t${ownerCount}transfer_date" name="t${ownerCount}transfer_date">
            </td>
            <td>
                <button type="button" class="remove-owner-row">✖</button> <!-- Cross button -->
            </td>
        `;

        table.appendChild(row);
        ownerCount++; // Increment the count for the next owner.

        // Add event listener to the remove button
        row.querySelector(".remove-owner-row").addEventListener("click", () => {
            row.remove(); // Remove the row
            reinitializeOwnerRowNumbers(); // Reinitialize the row numbers after removal
        });

    } else {
        alert("You can only add up to 12 owners.");
    }
});

// Function to reinitialize the owner row numbers
function reinitializeOwnerRowNumbers() {
    const rows = table.querySelectorAll("tr:nth-child(n+2)"); // Skip the header row
    ownerCount = 1; // Reset owner count for reinitialization

    rows.forEach((row, index) => {
        row.querySelector("td:first-child").textContent = `Owner ${ownerCount}`;
        ownerCount++;
    });
}




// Area Table Logic
let areaCount = 2; // Start with Area 1
const maxAreas = 11; // Maximum allowed areas (as per your prompt)

// Create the table structure initially
const areaDetails = document.getElementById("areaDetails");
const areaTable = document.createElement("table");
areaTable.setAttribute("border", "1");
areaTable.style.width = "100%";

// Add table headers
const areaHeaderRow = document.createElement("tr");
areaHeaderRow.innerHTML = `
    <th>Area</th>
    <th>Length (in sq metres)</th>
    <th>Width (in sq metres)</th>
    <th>Calculated Area</th>
    <th>Actions</th> <!-- Added column for actions -->
`;
areaTable.appendChild(areaHeaderRow);
areaDetails.appendChild(areaTable);

// Create the first row (always visible and required)
const firstRow = document.createElement("tr");

firstRow.innerHTML = `
    <td>Area 1</td>
    <td><input type="number" id="length1" placeholder="Enter Length" oninput="calculateArea(1)" required></td>
    <td><input type="number" id="width1" placeholder="Enter Width" oninput="calculateArea(1)" required></td>
    <td id="calculatedArea1">0</td>
    <td></td> <!-- No action button for the first row -->
`;

areaTable.appendChild(firstRow); // Append the first row to the table

// Event listener for adding new rows
document.getElementById("addArea").addEventListener("click", () => {
    if (areaCount >= maxAreas) {
        alert("You can only add up to 10 areas."); // Matches your original alert message
        return; // Prevent adding more rows
    }

    const row = document.createElement("tr");

    row.innerHTML = `
        <td>Area ${areaCount} </td>
        <td>
            <input type="number" id="length${areaCount}" placeholder="Enter Length" 
                   oninput="calculateArea(${areaCount})" required>
        </td>
        <td>
            <input type="number" id="width${areaCount}" placeholder="Enter Width" 
                   oninput="calculateArea(${areaCount})" required>
        </td>
        <td id="calculatedArea${areaCount}">0</td>
        <td>
            <button type="button" class="remove-row">✖</button> <!-- Cross button -->
        </td>
    `;

    // Append the row to the table
    areaTable.appendChild(row);

    // Increment the count for the next area
    areaCount++;

    // Add event listener to the remove button
    row.querySelector(".remove-row").addEventListener("click", () => {
        row.remove(); // Remove the row
        reinitializeAreaRowNumbers(); // Reinitialize the area row numbers after removal
    });
});

// Function to reinitialize the area row numbers
function reinitializeAreaRowNumbers() {
    const rows = areaTable.querySelectorAll("tr:nth-child(n+2)"); // Skip the header row
    areaCount = 2; // Start from 2 for subsequent rows

    rows.forEach((row, index) => {
        row.querySelector("td:first-child").textContent = `Area ${areaCount}`;
        areaCount++;
    });
}

// Function to calculate area dynamically
function calculateArea(count) {
    const length = document.getElementById(`length${count}`).value;
    const width = document.getElementById(`width${count}`).value;
    const areaCell = document.getElementById(`calculatedArea${count}`);

    // Calculate the area if length and width are valid
    if (length && width) {
        areaCell.textContent = (length * width).toFixed(2);
    } else {
        areaCell.textContent = "0"; // Default value when inputs are empty
    }
}
