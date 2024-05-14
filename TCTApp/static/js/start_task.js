// Get the elements for opening and closing modal
const openButton = document.querySelector("[data-open-modal]");
const closeButton = document.querySelector("[data-close-modal]");
const modal = document.querySelector('[data-modal]');

// Get the elements for opening and closing modal2
const openButton2 = document.querySelector("[data-open-modal2]");
const closeButton2 = document.querySelector("[data-close-modal2]");
const modal2 = document.querySelector('[data-modal2]');

// Get the elements for opening and closing modal5
const openButton5 = document.querySelector("[data-open-modal5]");
const closeButton5 = document.querySelector("[data-close-modal5]");
const modal5 = document.querySelector('[data-modal5]');

// // Add event listener to show confirmation dialog when leaving the page
// window.addEventListener('beforeunload', function(e) {
//     e.preventDefault();
//     e.returnValue = 'Leaving this page? Are you sure you want to navigate away from this page?';
// });

// Add event listener to open modal
openButton.addEventListener("click", () => {
    modal.showModal(); // Show modal when clicked
});

// Add event listener to close modal
closeButton.addEventListener("click", () => {
    modal.close(); // Close modal when clicked
});

// Add event listener to open modal2
openButton2.addEventListener("click", () => {
    modal2.showModal(); // Show modal2 when clicked
});

// Add event listener to close modal2
closeButton2.addEventListener("click", () => {
    modal2.close(); // Close modal2 when clicked
});


// Add event listener to open modal2
openButton5.addEventListener("click", () => {
    modal5.showModal(); // Show modal5 when clicked
});

// Add event listener to close modal2
closeButton5.addEventListener("click", () => {
    modal5.close(); // Close modal5 when clicked
});
