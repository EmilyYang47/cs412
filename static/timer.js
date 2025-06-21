const durationElem = document.getElementById("time_display");
const duration = parseInt(durationElem.textContent);
let timeLeft = duration;
let timer = null;
let currentState = "Start";

function updateDisplay() {
  const minutes = String(Math.floor(timeLeft / 60)).padStart(2, "0");
  const seconds = String(timeLeft % 60).padStart(2, "0");
  document.getElementById("time_display").textContent = `${minutes}:${seconds}`;
}

function startTimer() {
  if (timer) return;
  startTimestamp = Date.now();

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

function pauseTimer() {
  clearInterval(timer);
  timer = null;
  currentState = "Resume";
  updateControlButton();
}

function resumeTimer() {
  startTimer();
  currentState = "Pause";
  updateControlButton();
}

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

function handleControlClick() {
  if (currentState === "Start") {
    startTimer();
    currentState = "Pause";
  } else if (currentState === "Pause") {
    pauseTimer();
  } else if (currentState === "Resume") {
    resumeTimer();
  } else if (currentState === "End Session") {
    window.location.href = "/project/todo_list";
    return;
  }
  updateControlButton();
}

document.addEventListener("DOMContentLoaded", () => {
  updateDisplay();
  updateControlButton();

  document
    .getElementById("control_btn")
    .addEventListener("click", handleControlClick);
});
