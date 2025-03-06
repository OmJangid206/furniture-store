// Function to automatically dismiss the alert after 5 seconds
setTimeout(function () {
    var alertMessage = document.getElementById('alert-message');
    alertMessage.classList.add('fadeOut');
}, 5000);

// Function to handle custom close button
var customClose = document.getElementById('custom-close');
if (customClose) {
    customClose.onclick = function () {
        var alertMessage = document.getElementById('alert-message');
        alertMessage.classList.add('fadeOut');
    };
}

