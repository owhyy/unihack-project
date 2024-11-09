let seconds = 0;
let minutes = 0;
let hours = 0;
let timerInterval;
let totalTime = 0;

function formatTime(value) {
  return value < 10 ? `0${value}` : value;
}

function updateDisplay() {
  document.getElementById('display').textContent = 
    `${formatTime(hours)}:${formatTime(minutes)}:${formatTime(seconds)}`;
}

function startStopwatch() {
  if (!timerInterval) {
    timerInterval = setInterval(() => {
      seconds++;
      if (seconds === 60) {
        seconds = 0;
        minutes++;
      }
      if (minutes === 60) {
        minutes = 0;
        hours++;
      }
      updateDisplay();
    }, 1000);
  }
}

let time = document.getElementById("total-time");
async function stopStopwatch() {
  clearInterval(timerInterval);
  timerInterval = null;
  document.getElementById('display').textContent = "00:00:00"
  totalTime = hours * 3600 + minutes * 60 + seconds;
  time.innerText = totalTime + " seconds";
}

// Start the stopwatch automatically when the page loads
window.onload = startStopwatch;
