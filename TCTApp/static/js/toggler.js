// Variable to keep track of the state (expanded or minimized)
var state = "expanded";

// Function to handle the sidebar state based on the screen width
function handleSidebarState() {
  // Get the current screen width
  var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

  if (screenWidth <= 480) {
    if (state == "expanded") {
      minimizeSidebar();
    } else {
      expandSidebar();
    }
  } else if (screenWidth <= 768) {
    if (state == "expanded") {
      minimizeSidebar();
    } else {
      expandSidebar();
    }
  } else {
    if (state == "expanded") {
      minimizeSidebar();
    } else {
      expandSidebar();
    }
  }
}

// Function to minimize the sidebar by adjusting CSS properties
function minimizeSidebar() {
  $('.sidebar-menu').css('margin-left', '-230px');
  $('.sidebar-icon').css('margin-right', '11px');
  $('#record-table-max').css('margin-left', '-230px');
  $('#card-tasks').css('margin-left', '-50px');
  $('#record-table-max .card').css('margin-right', '-245px');
  $('#index-dashboard').css('margin-left', '-230px');
  $('#record-table-max #navbar-form-id').css('margin-left', '65.75vh');
  $('.sidebar-menu img').hide();
  $('#sb-top-border').hide();
  $('.sidebar-menu footer').hide();
  $('.sidebar-menu li').hide();
  state = "minimized";
}

// Function to expand the sidebar by adjusting CSS properties
function expandSidebar() {
  $('.sidebar-menu').css('margin-left', '0px');
  $('.sidebar-icon').css('margin-right', '20px');
  $('#record-table-max').css('margin-left', '0px');
  $('#record-table-max').css('width', '100%');
  $('#card-tasks').css('margin-left', '230px');
  $('#record-table-max #navbar-form-id').css('margin-left', '65.75vh');
  $('#index-dashboard').css('margin-left', '0px');
  $('.sidebar-menu img').show();
  $('#sb-top-border').show();
  $('.sidebar-menu footer').show();
  $('.sidebar-menu li').show();
  state = "expanded";
}

function minimizeSidebar2() {
  $('.sidebar-menu').css('margin-left', '-230px');
  $('.sidebar-icon').css('margin-right', '11px');
  $('#record-table-max').css('margin-left', '-230px');
  $('#card-tasks').css('margin-left', '-50px');
  $('#record-table-max .card').css('margin-right', '-245px');
  $('#index-dashboard').css('margin-left', '-230px');
  $('#record-table-max #navbar-form-id').css('margin-left', '65.75vh');
  $('.sidebar-menu img').hide();
  $('#sb-top-border').hide();
  $('.sidebar-menu footer').hide();
  $('.sidebar-menu li').hide();
  state = "minimized";
}

// Function to expand the sidebar by adjusting CSS properties
function expandSidebar2() {
  $('.sidebar-menu').css('margin-left', '0px');
  $('.sidebar-icon').css('margin-right', '20px');
  $('#record-table-max').css('margin-left', '0px');
  $('#record-table-max').css('width', '100%');
  $('#card-tasks').css('margin-left', '230px');
  $('#record-table-max #navbar-form-id').css('margin-left', '65.75vh');
  $('#index-dashboard').css('margin-left', '0px');
  $('.sidebar-menu img').show();
  $('#sb-top-border').show();
  $('.sidebar-menu footer').show();
  $('.sidebar-menu li').show();
  state = "expanded";
}

function minimizeSidebar3() {
  $('.sidebar-menu').css('margin-left', '-230px');
  $('.sidebar-icon').css('margin-right', '11px');
  $('#record-table-max').css('margin-left', '-230px');
  $('#card-tasks').css('margin-left', '-50px');
  $('#record-table-max .card').css('margin-right', '-245px');
  $('#index-dashboard').css('margin-left', '-230px');
  $('#record-table-max #navbar-form-id').css('margin-left', '65.75vh');
  $('.sidebar-menu img').hide();
  $('#sb-top-border').hide();
  $('.sidebar-menu footer').hide();
  $('.sidebar-menu li').hide();
  state = "minimized";
}

// Function to expand the sidebar by adjusting CSS properties
function expandSidebar3() {
  $('.sidebar-menu').css('margin-left', '0px');
  $('.sidebar-icon').css('margin-right', '20px');
  $('#record-table-max').css('margin-left', '0px');
  $('#record-table-max').css('width', '100%');
  $('#card-tasks').css('margin-left', '230px');
  $('#record-table-max #navbar-form-id').css('margin-left', '65.75vh');
  $('#index-dashboard').css('margin-left', '0px');
  $('.sidebar-menu img').show();
  $('#sb-top-border').show();
  $('.sidebar-menu footer').show();
  $('.sidebar-menu li').show();
  state = "expanded";
}

// Event handler for the click event on the sidebar-icon
$('.sidebar-icon').click(function() {
  handleSidebarState();
});

// // Handle the initial sidebar state on page load
// $(document).ready(function() {
//   handleSidebarState();
// });

// // Handle the sidebar state on window resize
// $(window).resize(function() {
//   handleSidebarState();
// });