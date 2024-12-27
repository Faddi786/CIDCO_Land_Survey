window.onload = function() {
    fetch('/userEdit_values_admin_panel')
      .then(response => response.json())
      .then(data => {
        console.log('me aa gaya');
        
        console.log(data);  // Log the data to check the structure
  
        // Populate the table with dynamic data
        const userTable = document.getElementById('userTable').getElementsByTagName('tbody')[0];
        const names = data.name;
        const phone_no = data.phone_no;
        const role = data.role;
        // const plotNos = data.Plot_No;  {}removing from user 
        const uids = data.userinfo_uid;
 
        names.forEach((namee, index) => {
          const row = userTable.insertRow();
  
          // Insert the serial number
          const srNoCell = row.insertCell(0);
          srNoCell.textContent = index + 1;

            // Insert the node name with the uid as a data attribute
            const nodeCell = row.insertCell(1);
            nodeCell.innerHTML = `
              <span class="data" data-uid="${uids[index]}">${namee}</span>
              <input type="text" class="edit-input" value="${namee}" style="display:none;">
            `;


          // Insert the phone_no
          const phone_noCell = row.insertCell(2);
          phone_noCell.innerHTML = `<span class="data">${phone_no[index]}</span><input type="text" class="edit-input" value="${phone_no[index]}" style="display:none;">`;
          // Insert the role
          const roleCell = row.insertCell(3);
          roleCell.innerHTML = `<span class="data">${role[index]}</span><input type="text" class="edit-input" value="${role[index]}" style="display:none;">`;
  
          // Insert the plot number 
        //   const plotCell = row.insertCell(4);  {}removing from user 
        //   plotCell.innerHTML = `<span class="data">${plotNos[index]}</span><input type="text" class="edit-input" value="${plotNos[index]}" style="display:none;">`;
  
          // Insert the actions cell (Edit/Delete/Update/Cancel)
          const actionsCell = row.insertCell(4);
          actionsCell.innerHTML = `
            <button class="editBtn" onclick="editRow(this)">Edit</button>
            <button class="updateBtn" onclick="updateRow(this)" style="display:none;">Update</button>
            <button class="cancelBtn" onclick="cancelRow(this)" style="display:none;">Cancel</button>
            <button class="deleteBtn" onclick="deleteRow(this)">Delete</button>
          `;
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

// Function to update the row with new values and send to Flask route
function updateRow(button) {
  var row = button.parentNode.parentNode;
  var inputs = row.querySelectorAll('input');
  var dataSpans = row.querySelectorAll('.data');
  
  // Collect the updated values from the inputs
  var updatedData = {};

  // Retrieve the UID from the input (this assumes the UID is stored in the data-uid of the input element)
  // Retrieve the UID from the span element (this assumes the UID is stored in the data-uid of the span element)
  const uid = dataSpans[0].getAttribute('data-uid'); // Assuming the first span holds the UID

  // Add the UID to the updated data object
  updatedData['uid'] = uid;

  // Collect the values from the input fields (excluding UID)
  inputs.forEach((input, index) => {
      updatedData[`column${index + 1}`] = input.value.trim(); // Collecting the updated data from input fields
  });


  console.log("this isthe data")
  console.log(updatedData)

  // Send the updated data to the Flask route using fetch
  fetch('/update_userEdit_values', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updatedData) // Sending the data to the Flask route
  })
  .then(response => response.json())
  .then(data => {
    // If the update was successful, update the UI with the new values
    if (data.success) {
      inputs.forEach((input, index) => {
        const newValue = input.value.trim();
        dataSpans[index].textContent = newValue; // Update the span with the new value
      });

      // Hide the input fields and show the updated values
      inputs.forEach(input => input.style.display = 'none');
      dataSpans.forEach(span => span.style.display = 'inline-block');

      // Hide Update and Cancel buttons, show Edit button
      row.querySelector('.updateBtn').style.display = 'none';
      row.querySelector('.cancelBtn').style.display = 'none';
      row.querySelector('.editBtn').style.display = 'inline-block';
    } else {
      // Handle failure (optional)
      alert('Failed to update data');
    }
  })
  .catch(error => {
    console.error('Error updating data:', error);
    alert('An error occurred while updating the data.');
  });
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



// Function to delete a row
function deleteRow(button) {
  // Get the row that contains the button
  var row = button.parentNode.parentNode;
  
  // Get the UID from the data attribute of the node name (assuming it's in a span with class 'data')
  var uid_to_delete = row.querySelector('.data').getAttribute('data-uid');
  
  // Send a POST request with the UID to the backend
  fetch('/delete_user_values', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 'uid': uid_to_delete })
  })
  .then(response => response.json())
  .then(data => {
      console.log("i am here ",uid_to_delete);  // You can log or display the server's response
      
      // Remove the row from the table after deletion
      confirm('are you sure you want to delete the node ?')
      row.parentNode.removeChild(row);
  })
  .catch(error => console.error('Error:', error));
}

