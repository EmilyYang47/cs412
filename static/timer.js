// File: timer.js
// Author: Emily Yang (eyang4@bu.edu), 6/18/2025
// Description: The timer js file which creates the timer for a study session.

const durationElem = document.getElementById("time_display");
const duration = parseInt(durationElem.textContent) * 60;
let timeLeft = duration;
let timer = null;
let currentState = "Start";

// update the time display of the timer
function updateDisplay() {
  const minutes = String(Math.floor(timeLeft / 60)).padStart(2, "0");
  const seconds = String(timeLeft % 60).padStart(2, "0");

  const h4 = document.querySelector("#time_display .timer-text");
  if (h4) {
    h4.textContent = `${minutes}:${seconds}`;
  }
}

// For every second, decrease the remaining time by one second.
function startTimer() {
  if (timer) return;
  startTimestamp = Date.now();

  // When the time is up, terminate the timer and prompt a notation
  // notifying the time is up.
  timer = setInterval(() => {
    if (timeLeft <= 0) {
      clearInterval(timer);
      timer = null;
      alert("Time's Up!");
      currentState = "End Session";
      updateControlButton();
      return;
    }
    timeLeft--;
    updateDisplay();
  }, 1000);
}

// The function to fause the timer.
function pauseTimer() {
  clearInterval(timer);
  timer = null;
  currentState = "Resume";
  updateControlButton();
}

// The function to resume the timer.
function resumeTimer() {
  startTimer();
  currentState = "Pause";
  updateControlButton();
}

// The function to update the button based on current status.
function updateControlButton() {
  const btn = document.getElementById("control_btn");
  if (currentState === "Start") {
    btn.textContent = "Start";
  } else if (currentState === "Pause") {
    btn.textContent = "Pause";
  } else if (currentState === "Resume") {
    btn.textContent = "Resume";
  } else if (currentState === "End Session") {
    btn.textContent = "End Session";
  }
}

// The function to handle button click, implementing the corresponding
// function when the button is clicked.
function handleControlClick() {
  if (currentState === "Start") {
    startTimer();
    currentState = "Pause";
  } else if (currentState === "Pause") {
    pauseTimer();
  } else if (currentState === "Resume") {
    resumeTimer();
  } else if (currentState === "End Session") {
    window.location.href = "/eyang4/project/todo_list";
    return;
  }
  updateControlButton();
}

// Pass the needed variables into the templates.
document.addEventListener("DOMContentLoaded", () => {
  updateDisplay();
  updateControlButton();

  document
    .getElementById("control_btn")
    .addEventListener("click", handleControlClick);
});
