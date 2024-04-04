

const usernameInput = document.getElementById('username');
const errorMessage = document.getElementById('error-message');

function validateInput() {
    const value = usernameInput.value.trim();
    // Check if the input is empty or contains invalid characters
    if (value === '' || !/^[a-zA-Z0-9]+$/.test(value)) {
        errorMessage.textContent = 'Please enter a valid username.';
        return false;
    } else {
        errorMessage.textContent = '';
        return true;
    }
}

usernameInput.addEventListener('blur', validateInput);