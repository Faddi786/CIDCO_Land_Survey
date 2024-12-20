window.onload = function() {
    fetch('/dropdown_values_admin_panel')
      .then(response => response.json())
      .then(data => {
        console.log(data);  // Log the data to check the structure
  
        // Populate the table with dynamic data
        const nodeTable = document.getElementById('nodeTable').getElementsByTagName('tbody')[0];
        const nodeNames = data.Node_Name;
        const sectors = data.Sector;
        const blockNames = data.Block_Name;
        const plotNos = data.Plot_No;
        const uids = data.dropdownvalues_uid; // Assuming the UID data is available in the response

        nodeNames.forEach((nodeName, index) => {
          const row = nodeTable.insertRow();
  
          // Insert the serial number
          const srNoCell = row.insertCell(0);
          srNoCell.textContent = index + 1;

          // Insert the node name with the uid as a data attribute
          const nodeCell = row.insertCell(1);
          nodeCell.innerHTML = `
            <span class="data" data-uid="${uids[index]}">${nodeName}</span>
            <input type="text" class="edit-input" value="${nodeName}" style="display:none;">
          `;

  
          // Insert the sector
          const sectorCell = row.insertCell(2);
          sectorCell.innerHTML = `<span class="data">${sectors[index]}</span><input type="text" class="edit-input" value="${sectors[index]}" style="display:none;">`;
  
          // Insert the block name
          const blockCell = row.insertCell(3);
          blockCell.innerHTML = `<span class="data">${blockNames[index]}</span><input type="text" class="edit-input" value="${blockNames[index]}" style="display:none;">`;
  
          // Insert the plot number
          const plotCell = row.insertCell(4);
          plotCell.innerHTML = `<span class="data">${plotNos[index]}</span><input type="text" class="edit-input" value="${plotNos[index]}" style="display:none;">`;
  
          // Insert the actions cell (Edit/Delete/Update/Cancel)
          const actionsCell = row.insertCell(5);
          actionsCell.innerHTML = `
            <button class="editBtn" onclick="editRow(this)">Edit</button>
            <button class="updateBtn" onclick="updateDropdownValues(this)" style="display:none;">Update</button>
            <button class="cancelBtn" onclick="cancelRow(this)" style="display:none;">Cancel</button>
            <button class="deleteBtn" onclick="deleteRow(this)">Delete</button>
          `;

          // Insert the hidden UID column
          const uidCell = row.insertCell(6);
          console.log("this is the uid")

          console.log(`${uids[index]}`)
          uidCell.innerHTML = `<input type="hidden" class="uid" value="${uids[index]}">`; // Hidden input for UID
            
        });
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
};

// Function to enable editing of the row
function editRow(button) {
    var row = button.parentNode.parentNode;
    var inputs = row.querySelectorAll('input');
    var dataSpans = row.querySelectorAll('.data');
    
    // Show the inputs and hide the text (span) elements
    inputs.forEach(input => input.style.display = 'inline-block');
    dataSpans.forEach(span => span.style.display = 'none');
  
    // Hide Edit button, show Update and Cancel buttons
    row.querySelector('.editBtn').style.display = 'none';
    row.querySelector('.updateBtn').style.display = 'inline-block';
    row.querySelector('.cancelBtn').style.display = 'inline-block';
}

// Function to cancel the edit and revert to the original values
function cancelRow(button) {
    var row = button.parentNode.parentNode;
    var inputs = row.querySelectorAll('input');
    var dataSpans = row.querySelectorAll('.data');
    
    // Get the original values from the spans and restore them in the input fields
    dataSpans.forEach((span, index) => {
        inputs[index].value = span.textContent.trim();
    });
    
    // Hide the input fields and show the original text (span) elements
    inputs.forEach(input => input.style.display = 'none');
    dataSpans.forEach(span => span.style.display = 'inline-block');
  
    // Hide Cancel and Update buttons, show Edit button
    row.querySelector('.cancelBtn').style.display = 'none';
    row.querySelector('.updateBtn').style.display = 'none';
    row.querySelector('.editBtn').style.display = 'inline-block';
}



// Function to update the data in the database
function updateDropdownValues(button) {
  console.log(button)
  console.log("this is the value")


  // Get the row where the delete button was clicked
  var row = button.parentNode.parentNode;
    
  console.log("this is the row value")
  console.log(row)
  // Check the values using console.log to debug
  const nodeName = row.querySelector('td:nth-child(1) input.edit-input').value;
  const sector = row.querySelector('td:nth-child(2) input.edit-input').value;
  const blockName = row.querySelector('td:nth-child(3) input.edit-input').value;
  const plotNo = row.querySelector('td:nth-child(4) input.edit-input').value;
  
  

  // Create an object with the updated data
  const updatedData = {
      node_name: nodeName,
      sector: sector,
      block_name: blockName,
      plot_no: plotNo
  };

console.log("values for updating")
console.log(updatedData)

  // Send the data to the backend API using fetch (POST request)
  fetch('/update_dropdown_values', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(updatedData)  // Send the data as JSON
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    
      if (data.success) {
          alert('Data updated successfully!');
      } else {
          alert('Failed to update data.');
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while updating the data.');
  });
}



// Function to delete a row
function deleteRow(button) {
  // Get the row where the delete button was clicked
  var row = button.parentNode.parentNode;
  
  // Get the uid from the hidden input inside the node name cell (6th column)
  var uid = row.querySelector('td:nth-child(2) .data').getAttribute('data-uid'); // Extract the uid from data-uid attribute
  
  // Log the uid to be deleted
  console.log("UID to delete:", uid);

  // Optionally, send the uid to the server
  fetch('/delete_values', {
      method: 'POST', // Or use GET if you prefer
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ uid: uid })
  })
  .then(response => response.json())
  .then(data => {
      console.log("Server response:", data);
  })
  .catch(error => {
      console.error('Error:', error);
  });
}
