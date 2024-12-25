    let ownerCount = 0;

    document.getElementById("addOwner").addEventListener("click", () => {
        if (ownerCount <= 12) {
            const container = document.createElement("div");
            container.innerHTML = `
                <h3>Owner ${ownerCount + 1}</h3>
                <label for="t${ownerCount}owner_name">Name of Owner ${ownerCount + 1}:</label>
                <input type="text" id="t${ownerCount}owner_name" name="t${ownerCount}owner_name">

                <label for="t${ownerCount}owner_transferdate">Date of Transfer:</label>
                <input type="date" id="owner${ownerCount}TransferDate" name="owner${ownerCount}TransferDate">
            `;
            document.getElementById("transferDetails").appendChild(container);
            ownerCount++;
        } else {
            alert("You can only add up to 12 owners.");
        }
    });

    function validateAndNext(current) {
        const section = document.getElementById(`section${current}`);
        const inputs = section.querySelectorAll("input, select, textarea");
        // for (const input of inputs) {
        //     if (!input.value) {
        //         alert("Please fill all fields before proceeding.");
        //         return;
        //     }
        // }
        document.getElementById(`section${current}`).classList.remove('active');
        document.getElementById(`section${current + 1}`).classList.add('active');
    }


    // Add an event listener to submit the form
document.getElementById("plotForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission
    submitFormData(); // Call the function to send the form data using XHR
});





// Function to validate and submit the form
function submitFormData() {
    // Create a new FormData object
    var formData = new FormData(document.getElementById("plotForm"));

    console.log("Form data before processing:");
    console.log([...formData.entries()]); // Log form data before adding defaults

    // Ensure all required fields exist (t1 to t12 owner_name and transfer_date)
    for (let i = 1; i <= 12; i++) {
        const ownerNameKey = `t${i}owner_name`;
        const transferDateKey = `t${i}transfer_date`;

        // If the field doesn't exist in formData, set a default value "-"
        if (!formData.has(ownerNameKey)) {
            formData.set(ownerNameKey, '-');
        }
        if (!formData.has(transferDateKey)) {
            formData.set(transferDateKey, '-');
        }
    }

    console.log("Form data after ensuring all required fields:");
    console.log([...formData.entries()]); // Log form data after processing

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









	 function prevSection(sectionId) {
            document.querySelector(`section#section${sectionId}`).classList.remove('active');
            document.getElementById(`section${sectionId - 1}`).classList.add('active');
        }
