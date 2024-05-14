// Get the submit button and form elements
const Req = document.getElementById('submit-req-edit');
const formReq = document.getElementById('record-edit-form');

// Add click event listener to the submit button
Req.addEventListener('click', () => {
  // Display a confirmation dialog
  if (confirm('Are you sure you want to edit this record?')) {
    // If the user confirms, submit the form
    formReq.submit();
  }
});