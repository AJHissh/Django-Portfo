$(document).ready(function() {
  // Flag to track if the mouse is being dragged
  var isDragging = false;

  // Variables to store initial values
  var startX, startY, scrollLeft, scrollTop;

  // Event handler for the 'mousedown' event
  $('.table-responsive').on('mousedown', function(e) {
    // Set the dragging flag to true
    isDragging = true;

    // Store the initial X position of the mouse
    startX = e.pageX;

    // Store the initial Y position of the mouse
    startY = e.pageY;

    // Store the initial horizontal scroll position
    scrollLeft = $(this).scrollLeft();

    // Store the initial vertical scroll position
    scrollTop = $(this).scrollTop();
  })

  // Event handler for the 'mouseup' event
  .on('mouseup', function(e) {
    // Set the dragging flag to false when the mouse is released
    isDragging = false;
  })

  // Event handler for the 'mousemove' event
  .on('mousemove', function(e) {
    // If not dragging, exit the function
    if (!isDragging) {
      return;
    }

    // Calculate the horizontal distance moved
    var deltaX = e.pageX - startX;

    // Calculate the vertical distance moved
    var deltaY = e.pageY - startY;

    // Adjust the horizontal scroll position based on the mouse movement
    $(this).scrollLeft(scrollLeft - deltaX);

    // Adjust the vertical scroll position based on the mouse movement
    $(this).scrollTop(scrollTop - deltaY);
  });
});
