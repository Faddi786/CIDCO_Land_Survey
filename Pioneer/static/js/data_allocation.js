window.onload = async function () {
    try {
        const response = await fetch('/onload_manage_sector');
        const data = await response.json();
             // Filter the data to only include rows where sectortable_isactive is 1
             const filteredData = data.filter(row => row.sectortable_isactive === 1);

        const tableBody = document.querySelector('#dataTable tbody');
        tableBody.innerHTML = ''; // Clear existing rows

        filteredData.forEach((row, index) => {

            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td id="user_${index}" class="editable" data-original="${row.user_name}" data-uid = "${row.sectortable_uid}" >${row.user_name}</td>
                <td id="sector_${index}" class="editable" data-original="${row.sector_name}">${row.sector_name}</td>
                <td id="phone_${index}" class="editable" data-original="${row.phone_no}">${row.phone_no}</td>
                <td id="uid_${index}" class="hidden" data-original="${row.sectortable_uid}">${row.sectortable_uid}</td>
                <td id="sect_value_${index}" class="hidden" data-original="${row.sectortable_isactive}">${row.sectortable_isactive}</td>
                <td>
                    <button onclick="editRow(this)">Edit</button>
                    <button onclick="deleteRow(this)" class="hidden">Delete</button>
                    <button onclick="saveRow(this)" class="hidden">Save</button>
                    <button onclick="cancelEdit(this)" class="hidden">Cancel</button>
                </td>
            `;

            tableBody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

// Filter function for the table
function filterTable() {
    var filter = document.getElementById("usernameFilter").value.toLowerCase();
    var rows = document.getElementById("dataTable").getElementsByTagName("tr");

    for (var i = 1; i < rows.length; i++) {
        var cell = rows[i].getElementsByTagName("td")[0]; // Username column
        if (cell) {
            var textValue = cell.textContent || cell.innerText;
            rows[i].style.display = textValue.toLowerCase().indexOf(filter) > -1 ? "" : "none";
        }
    }
}

// Edit row function
function editRow(btn) {
    const row = btn.closest("tr");

    // Make cells editable
    row.querySelectorAll(".editable").forEach(cell => {
        cell.contentEditable = "true";
        //cell.style.backgroundColor = "#f0f0f0"; // Highlight when editable
    });

    // Show save, delete, cancel buttons and hide edit button
    toggleButtons(btn, ["inline", "inline", "inline", "none"]);
}

// Save the row (update the data in the database)
async function saveRow(btn) {
    const row = btn.closest("tr");

    // Access the username, sector name, and phone number
    const username = row.querySelector('td[id^="user_"]').textContent.trim();
    const sectorName = row.querySelector('td[id^="sector_"]').textContent.trim();
    const phoneNo = row.querySelector('td[id^="phone_"]').textContent.trim();

    // Access the UID from the username column
    const sectortableUid = row.querySelector('td[id^="user_"]').getAttribute('data-uid');

    // Log the accessed values
    console.log("Username:", username);
    console.log("Sector Name:", sectorName);
    console.log("Phone Number:", phoneNo);
    console.log("sectortableUid", sectortableUid);


    // Send a POST request to update the data
    try {
        const response = await fetch('/update_values', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sectortableUid: sectortableUid,
                username: username,
                sectorName: sectorName,
                phoneNo: phoneNo
            })
        });

        const data = await response.json();

        // Handle the response from the server
        if (data.message === 'Record updated successfully') {

            alert("Record updated successfully")
            //window.location.reload()

        } else {
            alert('Error updating row');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}


// Cancel edit and revert changes
function cancelEdit(btn) {
    const row = btn.closest("tr");

    // Revert content to original values
    row.querySelectorAll(".editable").forEach(cell => {
        const originalValue = cell.getAttribute("data-original"); // Get the original value
        cell.textContent = originalValue; // Revert to original value
        cell.contentEditable = "false"; // Make cell non-editable
        cell.style.backgroundColor = ""; // Remove background highlight
    });

    // Restore the default view
    toggleButtons(btn, ["none", "none", "none", "inline"]);
}

// Delete row function

// Function to delete a row
async function deleteRow(button) {

    const isConfirmed = confirm("Are you sure you want to delete this row?");
    if (!isConfirmed) {
            // Restore the default view
    toggleButtons(button, ["none", "none", "none", "inline"]);
        return; // If the user cancels, exit the function
    }
    
    // Get the row that contains the button
    var row = button.closest('tr');
    
    // Get the sectortable_uid from the hidden column (the fourth <td> with the 'hidden' class)
    var sectortable_uid_to_delete = row.querySelector('.hidden').textContent;
  
    // Log the UID to verify it's being correctly retrieved
    console.log("sectortable_uid_to_delete: ", sectortable_uid_to_delete);
    
    if (!sectortable_uid_to_delete) {
      console.error("Error: sectortable_uid is not found.");
      return;
    }
  
    // Send a POST request with the sectortable_uid to the backend
    try {
      const response = await fetch('/delete_values', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'sectortable_uid': sectortable_uid_to_delete })
      });
      
      const data = await response.json();
      
      console.log("Response from server:", data);  // Log server response
      
      if (data.message === 'Record updated successfully') {
        // Remove the row from the table after successful deletion
        row.parentNode.removeChild(row);
      } else {
        alert('Error deleting row');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
  
  


// Utility function to toggle button visibility
function toggleButtons(button, states) {
    const buttons = button.parentElement.querySelectorAll("button");
    buttons[0].style.display = states[3]; // Edit button
    buttons[1].style.display = states[0]; // Delete button
    buttons[2].style.display = states[1]; // Save button
    buttons[3].style.display = states[2]; // Cancel button
}
