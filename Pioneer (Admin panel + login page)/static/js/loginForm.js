function login() {
    // Get the value of the phone number input field
    const phoneNo = document.getElementById('phone_no').value;

    // Ensure the entered phone number is a valid 10-digit number
    const phonePattern = /^[0-9]{10}$/;

    // Check if the phone number matches the pattern
    if (!phonePattern.test(phoneNo)) {
        alert("Please enter a valid 10-digit phone number.");
        return;  // Prevent form submission if the phone number is invalid
    }

    // Convert phone number input to an integer for comparison
    const phoneNoInt = parseInt(phoneNo, 10);

    // Fetch the users' data from the backend API
    fetch('/phone_no_validation')
        .then(response => response.json())
        .then(data => {
            console.log("Data from server:", data);

            // Assuming the data returned from the backend has a 'users' array with all user objects
            const usersFromDb = data.users;

            // Find the user object by matching the phone number
            const user = usersFromDb.find(user => user.phone_no === phoneNoInt);

            // If the user is not found, display an error
            if (!user) {
                alert("User not found! Please enter a valid registered phone number.");
                return;  // Prevent form submission if the phone number is not found
            }

            // If the phone number is valid and found in the database, check the role
            if (user.role === 0) {
                // If role is 0, redirect to the user page
                window.location.href = "/survey_user";  // Redirect to user.html
            } else if (user.role === 1) {
                // If role is 1, redirect to the manager page
                window.location.href = "/qc_user";  // Redirect to manager.html
            } else if (user.role === 2) {
                // If role is 1, redirect to the manager page
                window.location.href = "/validator_user";  // Redirect to manager.html
            } else if (user.role === 3) {
                // If role is 1, redirect to the manager page
                window.location.href = "/admin_user";  // Redirect to manager.html
            } else {
                alert("User role is invalid.");
            }

            // Optionally, you can now access the full user object for further processing
            console.log("User details:", user);
        })
        .catch(error => {
            console.error("Error fetching users:", error);
            alert("An error occurred while validating the phone number. Please try again.");
        });
}


