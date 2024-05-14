document.querySelectorAll('.start_popup').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
    
        if (confirm("Clicking okay will start the time for your task, are you sure you want to start?")) {
            window.location.href = this.getAttribute('href');
        }
    });
});