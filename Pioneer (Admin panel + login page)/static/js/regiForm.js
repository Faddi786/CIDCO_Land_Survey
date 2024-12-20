const form = document.getElementById('login-form');

form.addEventListener('submit', function(event) {
    event.preventDefault();

    // Clear previous errors
    document.getElementById('username-error').textContent = '';
    document.getElementById('phonenumber-error').textContent = '';
    document.getElementById('user_id-error').textContent = '';
    document.getElementById('role-error').textContent = '';

    let valid = true;

    // Validate Username
    const username = document.getElementById('username').value;
    if (username === '') {
        document.getElementById('username-error').textContent = 'Username is required.';
        valid = false;
    }

    // Validate Phone Number
    const phoneNumber = document.getElementById('phonenumber').value;
    const phonePattern = /^[0-9]{10}$/;
    if (!phonePattern.test(phoneNumber)) {
        document.getElementById('phonenumber-error').textContent = 'Please enter a valid 10-digit phone number.';
        valid = false;
    }

    // Validate User ID
    const userId = document.getElementById('user_id').value;
    if (userId === '') {
        document.getElementById('user_id-error').textContent = 'User ID is required.';
        valid = false;
    }

    // Validate Role
    const role = document.getElementById('role').value;
    if (role === '') {
        document.getElementById('role-error').textContent = 'Please select a role.';
        valid = false;
    }

    if (valid) {
        alert('Form submitted successfully!');
    }
});