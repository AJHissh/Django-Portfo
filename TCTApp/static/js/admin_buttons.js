// Get the submit button and form element
const submitButton = document.getElementById('submit-edit');
const form = document.getElementById('record-edit-form');

// Add event listener to the submit button
submitButton.addEventListener('click', () => {
  // Display a confirmation dialog before submitting the form
  if (confirm('Are you sure you want to edit this record?')) {
    form.submit();
  }
});

// Add event listener to the delete button
document.getElementById("delete-record").addEventListener("click", function(event) {
  event.preventDefault();
  var form = document.getElementById("record-edit-form");
  var input = document.createElement("input");
  input.setAttribute("type", "hidden");
  input.setAttribute("name", "delete_record");
  input.setAttribute("value", "delete_record");
  form.appendChild(input);
  
  // Display a confirmation dialog before submitting the form
  if (confirm('Are you sure you want to delete this record?')) {
    form.submit();
  }
});

// Update the clock element with the current date and time
var clockElement = document.getElementById('clock');
function clock() {
    clockElement.textContent = new Date().toString();
    setInterval(clock, 1000);
}
