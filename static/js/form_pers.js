// Function to save form data to local storage
function saveFormData() {
  var formInputs = document.getElementById("task-form").elements;
  var formData = {};

  // Iterate through form inputs and store their values in the formData object
  for (var i = 0; i < formInputs.length; i++) {
    var input = formInputs[i];
    if (input.type !== "submit") {
      formData[input.name] = input.value;
    }
  }

  // Save the formData object as a JSON string in local storage
  localStorage.setItem("formData", JSON.stringify(formData));
}

// Function to populate form fields with saved data on page load
function populateForm() {
  var savedData = localStorage.getItem("formData");

  // If saved data exists, parse it and populate the form inputs
  if (savedData) {
    var formData = JSON.parse(savedData);
    var formInputs = document.getElementById("task-form").elements;

    for (var i = 0; i < formInputs.length; i++) {
      var input = formInputs[i];
      if (input.type !== "submit" && formData[input.name]) {
        input.value = formData[input.name];
      }
    }
  }
}

// Function to clear form data from local storage on form submission and submit the form
function clearFormDataAndSubmit() {
  // Remove saved form data from local storage
  localStorage.removeItem("formData");
  // Submit the form
  this.submit();
}

// Save form data when form inputs change
var formInputs = document.getElementById("task-form").elements;
for (var i = 0; i < formInputs.length; i++) {
  var input = formInputs[i];
  if (input.type !== "submit") {
    input.addEventListener("change", saveFormData);
  }
}

// Populate form on page load
window.addEventListener("load", populateForm);

// // Add event listener for form submission
// var form = document.getElementById("task-form");
// form.addEventListener("submit", clearFormDataAndSubmit);
