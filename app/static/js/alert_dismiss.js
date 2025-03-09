/*
  alert_dismiss.js - Handles automatic and manual dismissal of alert messages.
  This script provides functionality to automatically dismiss an alert message
  after a specified time and to manually dismiss it using a custom close button.
*/

// Automatically hides the alert message after 5 seconds.
setTimeout(function () {
    var alertMessage = document.getElementById('alert-message');
    alertMessage.classList.add('fadeOut');
}, 5000);

// Handles the custom close button click to manually hide the alert.
var customClose = document.getElementById('custom-close');
if (customClose) {
    customClose.onclick = function () {
        var alertMessage = document.getElementById('alert-message');
        if (alertMessage) { // Check if the element exists
            alertMessage.classList.add('fadeOut');
        }
    };
}
