window.onload = function() {
    var timerDiv = document.getElementById('timer');
    var startTime = new Date().getTime(); // get current time in milliseconds

    setInterval(function() {
        var currentTime = new Date().getTime(); // get current time in milliseconds
        var elapsedTime = currentTime - startTime; // calculate elapsed time in milliseconds

        // convert elapsed time to seconds, minutes, and hours
        var seconds = Math.floor(elapsedTime / 1000) % 60;
        var minutes = Math.floor(elapsedTime / 1000 / 60) % 60;
        var hours = Math.floor(elapsedTime / 1000 / 60 / 60);

        // display the timer in the format HH:MM:SS
        timerDiv.innerHTML = hours + ':' + minutes + ':' + seconds;
    }, 1000); // update the timer every second
}; 