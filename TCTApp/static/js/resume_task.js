// Get the elements for opening and closing modal3
const openButton3 = document.querySelector("[data-open-modal3]");
const closeButton3 = document.querySelector("[data-close-modal3]");
const modal3 = document.querySelector('[data-modal3]');

// Get the elements for opening and closing modal4
const openButton4 = document.querySelector("[data-open-modal4]");
const closeButton4 = document.querySelector("[data-close-modal4]");
const modal4 = document.querySelector('[data-modal4]');

// Add event listener to open modal3
openButton3.addEventListener("click", () => {
    modal3.showModal(); // Show modal3 when clicked
});

// Add event listener to close modal3
closeButton3.addEventListener("click", () => {
    modal3.close(); // Close modal3 when clicked
});

// Add event listener to open modal4
openButton4.addEventListener("click", () => {
    modal4.showModal(); // Show modal4 when clicked
});

// Add event listener to close modal4
closeButton4.addEventListener("click", () => {
    modal4.close(); // Close modal4 when clicked
});
