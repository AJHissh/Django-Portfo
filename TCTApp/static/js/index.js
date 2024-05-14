// Initialize elapsedTime variable
var elapsedTime = 0;

var buttons = document.querySelectorAll('#resume-button');
  buttons.forEach(function(button) {
    button.addEventListener('click', function(event) {
      var confirmed = confirm('Clicking okay will automatically start the time for your task, are you sure you want to resume the task? If task has already been started - time will continue until paused or submitted');
      if (!confirmed) {
        event.preventDefault(); // Prevent the default behavior (navigating to the href)
      }
    });
  });

// Add event listeners to start_download links
document.querySelectorAll('.start_download').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
    
        // Display a confirmation dialog before redirecting to the link's href
        setTimeout(function() {
            if (confirm("Download Starting - Please Press OK to continue")) {
                window.location.href = link.getAttribute('href');
            }
        }, 1);
    });
});

// Timer functionality
function startTimer(view) {
  var btn = document.getElementsByTagName("button")[0];
  var timerDiv = document.getElementById('timer');
  var formOpenTime = new Date().toLocaleString();
  var startTime = new Date().getTime();
  var pausedTime = 0;
  var timerInterval;

  // Check if there is a stored elapsed time for the specific view in local storage
  var viewElapsedTimeKey = 'elapsedTime_' + view;
  if (localStorage.getItem(viewElapsedTimeKey)) {
    elapsedTime = parseInt(localStorage.getItem(viewElapsedTimeKey));
    startTime = new Date().getTime() - elapsedTime;
  } else {
    startTime = new Date().getTime();
  }

  // Create and append a hidden input field for form_open_time
  var formOpenTimeField = document.createElement('input');
  formOpenTimeField.setAttribute('type', 'hidden');
  formOpenTimeField.setAttribute('name', 'form_open_time');
  formOpenTimeField.setAttribute('value', formOpenTime);
  document.getElementById('task-form').appendChild(formOpenTimeField);

  // Update the timer every second
  timerInterval = setInterval(updateTimerDisplay, 1000);

  var isPausing = false;
  // Add event listeners to pause, resume, end, and edit_submit buttons
  document.getElementById('pause').addEventListener('click', function() {
    var pauseButton = this;
  
    // Check if form submission is already in progress
    if (isPausing) {
      return;
    }
  
    // Disable the button
    pauseButton.disabled = true;
  
    // Set the flag to indicate form submission is in progress
    isPausing = true;
    pauseTimer(view);
  });

  
  document.getElementById('resume').addEventListener('click', resumeTimer);
  
  var isSubmitting = false;
  document.getElementById('end').addEventListener('click', function() {
    var endButton = this;
  
    // Check if form submission is already in progress
    if (isSubmitting) {
      return;
    }
  
    // Disable the button
    endButton.disabled = true;
  
    // Set the flag to indicate form submission is in progress
    isSubmitting = true;
  
    // Call the endTimer function
    endTimer(view);
  });
  document.getElementById('edit_submit').addEventListener('click', editSubmit);

  // Update the timer display
  function updateTimerDisplay() {
    var currentTime = new Date().getTime();
    var elapsedTime = currentTime - startTime;

    var totalSeconds = Math.floor(elapsedTime / 1000);
    var seconds = totalSeconds % 60;
    var totalMinutes = Math.floor(totalSeconds / 60);
    var minutes = totalMinutes % 60;
    var hours = Math.floor(totalMinutes / 60);

    timerDiv.innerHTML = hours + ':' + minutes + ':' + seconds;

    // Save the elapsed time for the specific view in local storage
    localStorage.setItem(viewElapsedTimeKey, elapsedTime);
  }

  // Pause the timer and submit the form
  function pauseTimer(view) {
    var timerDiv = document.getElementById('timer');
    var elapsedTime = timerDiv.innerHTML; // Get the elapsed time from the timer display
  
    // Calculate the elapsed time in hours, minutes, and seconds
    var [hours, minutes, seconds] = elapsedTime.split(':');
    var viewElapsedTimeKey = 'elapsedTime_' + view;

    var viewDateOpenedKey = 'dateOpened_' + view;
    var dateOpened = localStorage.getItem(viewDateOpenedKey); // Retrieve the stored dateOpened value

    // Create and append hidden input fields for is_paused and elapsed_time
    var is_paused = document.createElement('input');
    is_paused.setAttribute('type', 'hidden');
    is_paused.setAttribute('name', 'is_paused');
    is_paused.setAttribute('value', 'True');
    document.getElementById('task-form').appendChild(is_paused);

    var elapsed_time_field = document.createElement('input');
    elapsed_time_field.setAttribute('type', 'hidden');
    elapsed_time_field.setAttribute('name', 'elapsed_time');
    elapsed_time_field.setAttribute('value', hours + ':' + minutes + ':' + seconds);
    document.getElementById('task-form').appendChild(elapsed_time_field);

    var date_opened_field = document.createElement('input');
    date_opened_field.setAttribute('type', 'hidden');
    date_opened_field.setAttribute('name', 'date_opened');
    date_opened_field.setAttribute('value', dateOpened);
    document.getElementById('task-form').appendChild(date_opened_field);

    localStorage.removeItem("formData");
    localStorage.removeItem(viewElapsedTimeKey);
    localStorage.removeItem(viewDateOpenedKey);
    clearInterval(timerInterval);

    // Submit the form
    document.getElementById('task-form').submit();
    
  }

  // Resume the timer
  function resumeTimer() {
    startTime = new Date().getTime() - elapsedTime - pausedTime;
    timerInterval = setInterval(updateTimer, 1000);
    document.getElementById('resume').style.display = 'none';
    document.getElementById('pause').style.display = 'block';
    document.getElementById('end').style.display = 'block';
  }

  // End the timer and submit the form
  // End the timer and submit the form
  function endTimer(view) {
    var timerDiv = document.getElementById('timer');
    var elapsedTime = timerDiv.innerHTML; // Get the elapsed time from the timer display
  
    // Calculate the elapsed time in hours, minutes, and seconds
    var [hours, minutes, seconds] = elapsedTime.split(':');
    var viewElapsedTimeKey = 'elapsedTime_' + view;
  
    var viewDateOpenedKey = 'dateOpened_' + view;
    var dateOpened = localStorage.getItem(viewDateOpenedKey); // Retrieve the stored dateOpened value
  
  
    // Create and append hidden input fields for elapsed_time and date_opened
    var elapsed_time_field = document.createElement('input');
    elapsed_time_field.setAttribute('type', 'hidden');
    elapsed_time_field.setAttribute('name', 'elapsed_time');
    elapsed_time_field.setAttribute('value', hours + ':' + minutes + ':' + seconds);
    document.getElementById('task-form').appendChild(elapsed_time_field);
  
    var date_opened_field = document.createElement('input');
    date_opened_field.setAttribute('type', 'hidden');
    date_opened_field.setAttribute('name', 'date_opened');
    date_opened_field.setAttribute('value', dateOpened);
    document.getElementById('task-form').appendChild(date_opened_field);
  
    // Clear the timer update interval
  
    // Fetch request to submit the form data
    var form = document.getElementById('task-form');
    var formData = new FormData(form);
  
    fetch(form.action, {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          clearInterval(timerInterval);
          // Remove stored form data from local storage
          localStorage.removeItem(viewElapsedTimeKey);
          localStorage.removeItem('formData');
          window.location.href = data.redirect_url;
          localStorage.removeItem(viewDateOpenedKey);
        } else {
          displayErrors(data.errors);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  // Display error messages
  // Display error messages and handle "No" button click
  function displayErrors(errors) {
    var errorList = document.getElementById('error-list');
    errorList.innerHTML = '';
  
    for (var field in errors) {
      if (errors.hasOwnProperty(field)) {
        var errorMessages = errors[field];
        for (var i = 0; i < errorMessages.length; i++) {
          var errorMessage = errorMessages[i];
          var errorItem = document.createElement('li');
          errorItem.innerText = errorMessage;
          errorList.appendChild(errorItem);
        }
      }
    }
  
    var errorContainer = document.getElementById('error-container');
    errorContainer.style.display = 'block';
    };}
  

  document.addEventListener('DOMContentLoaded', function() {
    // Get all elements with the 'start_popup' class
    var startPopups = document.getElementsByClassName('start_popup');
  
    // Iterate over each start_popup element
    for (var i = 0; i < startPopups.length; i++) {
      var startPopup = startPopups[i];
      var view = startPopup.getAttribute('data-view');
      var timerDiv = startPopup.getElementsByClassName('timer')[0];
    
      // Get the stored elapsed time for the specific view from the local storage
      var viewElapsedTimeKey = 'elapsedTime_' + view;
      var elapsedTime = localStorage.getItem(viewElapsedTimeKey);
      var startTime;
    
      // Get the stored date_opened for the specific view from the local storage
      var viewDateOpenedKey = 'dateOpened_' + view;
      var dateOpened = localStorage.getItem(viewDateOpenedKey);

      if (dateOpened) {
        var dataIcon = startPopup.getElementsByClassName('data-icon')[0];
        if (!dataIcon) {
          var dataIcon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
          dataIcon.setAttribute('class', 'data-icon');
          dataIcon.setAttribute('height', '1.5em');
          dataIcon.setAttribute('viewBox', '0 0 450 700');

          var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          path.setAttribute('d', 'M0 24C0 10.7 10.7 0 24 0H360c13.3 0 24 10.7 24 24s-10.7 24-24 24h-8V67c0 40.3-16 79-44.5 107.5L225.9 256l81.5 81.5C336 366 352 404.7 352 445v19h8c13.3 0 24 10.7 24 24s-10.7 24-24 24H24c-13.3 0-24-10.7-24-24s10.7-24 24-24h8V445c0-40.3 16-79 44.5-107.5L158.1 256 76.5 174.5C48 146 32 107.3 32 67V48H24C10.7 48 0 37.3 0 24zM110.5 371.5c-3.9 3.9-7.5 8.1-10.7 12.5H284.2c-3.2-4.4-6.8-8.6-10.7-12.5L192 289.9l-81.5 81.5zM284.2 128C297 110.4 304 89 304 67V48H80V67c0 22.1 7 43.4 19.8 61H284.2z');

          // Set the fill attribute to change the color of the SVG path
          path.setAttribute('fill', '#33b249'); // Change the color to red (you can use any valid CSS color value)

          dataIcon.appendChild(path);

          // Append the dataIcon to the startPopup
          startPopup.appendChild(dataIcon);
        }
      }
    
      if (elapsedTime) {
        elapsedTime = parseInt(elapsedTime);
        startTime = elapsedTime;
      } else {
        startTime = new Date().getTime();
        elapsedTime = 0;
        localStorage.setItem(viewElapsedTimeKey, elapsedTime);
      }
    
      // Render the date_opened on the page
      var dateOpenedElement = startPopup.getElementsByClassName('date_opened')[0];
      if (dateOpenedElement) {
        dateOpenedElement.textContent = dateOpened;
      }
    
      // Attach click event listener to each start_popup link
      startPopup.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default link behavior
      
        if (!dateOpened) {
          dateOpened = new Date().toISOString();
          localStorage.setItem(viewDateOpenedKey, dateOpened);
        }

        setTimeout(function() {
          if (confirm("Clicking okay will automatically start the time for your task, are you sure you want to start the task? If task has already been started - time will continue until paused or submitted")) {
            var href = event.target.getAttribute('href'); // Get the link URL
            href += '&dateOpened=' + encodeURIComponent(dateOpened); // Append dateOpened parameter
            window.location.href = href; // Redirect to the new page with the dateOpened parameter
          }
      }, 1)});
      
      // Update the timer every second
      setInterval(updateTimerLogic, 1000);
    
      // Update the timer display
      function updateTimerLogic() {
        var currentTime = new Date().getTime();
        var elapsedTime = currentTime - startTime;
      
        var totalSeconds = Math.floor(elapsedTime / 1000);
        var seconds = totalSeconds % 60;
        var totalMinutes = Math.floor(totalSeconds / 60);
        var minutes = totalMinutes % 60;
        var hours = Math.floor(totalMinutes / 60);
      
        timerDiv.innerHTML = hours + ':' + minutes + ':' + seconds;
      }
    }
  });