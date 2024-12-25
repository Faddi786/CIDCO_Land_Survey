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
