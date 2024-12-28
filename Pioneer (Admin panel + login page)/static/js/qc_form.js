// Function to handle the "Accept and Push for Validation" button click
function acceptAndPushForValidation(formId) {
    // Display an alert confirming the action
    const userConfirmed = confirm("Are you sure you want to accept and push this for validation?");

    if (userConfirmed) {
        // Send data to the backend to update the database
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/update_status", true); // Replace '/update_status' with your actual API endpoint
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                alert("Data updated successfully!");
            } else if (xhr.readyState === 4) {
                alert("Error updating data. Please try again.");
            }
        };

        // Send the form ID and the status updates to the backend
        const data = {
            formId: formId,
            isQcDone: 1,
            surveyFormStatus: 1,
        };

        xhr.send(JSON.stringify(data));
    }
}

// Add event listener to the button (assuming the button has the ID 'acceptPushButton')
document.getElementById("acceptPushButton").addEventListener("click", function () {
    const formId = document.getElementById("surveyformdata_uid").value; 
    acceptAndPushForValidation(formId);
});



// Open modal for image
function openModal(image) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImg');
    modal.style.display = 'flex';
    modalImg.src = image.src;
}

// Close image modal
function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = 'none';
}


// copy the  main prt from editByQC.js file 

function fetchPlotDetails() {
    fetch('/get_outputform_data')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                console.log("This is the data");
                console.log(data);

                // Populate the fields with fetched data


                document.getElementById("surveyformdata_uid").textContent  = data.surveyformdata_uid || "No data";
                document.getElementById("entry_date_created").textContent  = data.entry_date_created || "No data";
                document.getElementById("user_name").textContent  = data.user_name || "No data";
                document.getElementById("node_name").textContent  = data.node_name || "No data";
                document.getElementById("sector_no").textContent  = data.sector_no || "No data";
                document.getElementById("block_name").value = data.block_name || "No data";
                document.getElementById("plot_name").textContent  = data.plot_name || "No data";
                document.getElementById("plot_status").textContent  = data.plot_status || "No data";
                document.getElementById("surveyor_remarks").textContent  = data.surveyor_remarks || "No data";
                document.getElementById("allotment_date").textContent  = data.allotment_date || "No data";
                document.getElementById("original_allottee").textContent  = data.original_allottee || "No data";
                document.getElementById("area").textContent  = data.area || "No data";
                document.getElementById("use_of_plot").textContent  = data.use_of_plot || "No data";
                document.getElementById("FSI").textContent  = data.FSI || "No data";
                document.getElementById("term_of_lease").textContent  = data.term_of_lease || "No data";
                document.getElementById("rate").textContent  = data.rate || "No data";
                
                // Handle photos
                document.getElementById("front_photo").src = data.front_photo ? 
                    `static/uploads/${data.front_photo}` : "static/uploads/default.png";
                document.getElementById("left_photo").src = data.left_photo ? 
                    `static/uploads/${data.left_photo}` : "static/uploads/default.png";
                document.getElementById("back_photo").src = data.back_photo ? 
                    `static/uploads/${data.back_photo}` : "static/uploads/default.png";
                document.getElementById("right_photo").src = data.right_photo ? 
                    `static/uploads/${data.right_photo}` : "static/uploads/default.png";
                document.getElementById("plot_sketch").src = data.plot_sketch ? 
                    `static/uploads/${data.plot_sketch}` : "static/uploads/default.png";
                
                // Optionally update alt text to handle missing photos
                document.getElementById("front_photo").alt = data.front_photo ? data.front_photo : "No Photo for front";
                document.getElementById("left_photo").alt = data.left_photo ? data.left_photo : "No Photo for left";
                document.getElementById("back_photo").alt = data.back_photo ? data.back_photo : "No Photo for back";
                document.getElementById("right_photo").alt = data.right_photo ? data.right_photo : "No Photo for right";
                document.getElementById("plot_sketch").alt = data.plot_sketch ? data.plot_sketch : "No Photo for sketch";

                // Initialize flag to check if any valid owner data exists
                let validOwnerDataExists = false;
                const transferDetailsDiv = document.getElementById("transferDetails");

               // Create table to display owner details in three columns
               const table = document.createElement("table");
               const tableHeader = document.createElement("tr");
               tableHeader.innerHTML = `
                   <th>Owner</th>
                   <th>Owner Name</th>
                   <th>Transfer Date</th>
               `;
               const headers = tableHeader.querySelectorAll('th');
headers.forEach(function(header) {
    header.style.border = '2px solid black';
    header.style.padding = '10px';
    header.style.backgroundColor = '#f2f2f2'; // Optional background color for better visibility
});

               table.appendChild(tableHeader);
               

               // Loop through the owners (up to 12)
               for (let i = 1; i <= 11; i++) {
                   const ownerNameKey = `t${i}owner_name`;
                   const transferDateKey = `t${i}transfer_date`;

                   const ownerName = data[ownerNameKey]; // Get owner name from fetched data
                   const transferDate = data[transferDateKey]; // Get transfer date from fetched data

                   // Check if both owner name and transfer date are valid (not null, empty, or '-')
                   if (ownerName && ownerName !== '-' && transferDate && transferDate !== '-') {
                       validOwnerDataExists = true;

                       // Create a table row for valid owner data
                       const row = document.createElement("tr");
                       row.innerHTML = `
                           <td>Owner ${i + 1}</td>  <!-- Start numbering from Owner 2 -->
                           <td><input type="text" value='${ownerName}'></input></td>
                           <td><input type="date" value='${transferDate}'></input></td>
                       `;
                       table.appendChild(row);
                   }
               }

               // Append the table to the transferDetails div
               transferDetailsDiv.appendChild(table);

               // Only display Section 3 if there is at least one valid owner data
               if (validOwnerDataExists) {
                   document.getElementById("section3").style.display = "block";
               }
           }
       })
       .catch(error => {
           alert("Error fetching plot details: " + error);
       });
}


window.onload = function() {
    fetchPlotDetails();  // Fetch data as soon as the page loads
};
