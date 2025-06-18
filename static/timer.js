let startTimestamp = null;
let accumulatedTime = 0;

let duration = 5; // 25 * 60 in real usage
let timeLeft = duration;
let timer = null;
let currentState = "Start"; // start, pause, resume

function updateDisplay() {
  const minutes = String(Math.floor(timeLeft / 60)).padStart(2, "0");
  const seconds = String(timeLeft % 60).padStart(2, "0");
  document.getElementById("time-display").textContent = `${minutes}:${seconds}`;
}

function startTimer() {
  if (timer) return;
  startTimestamp = Date.now();

  timer = setInterval(() => {
    if (timeLeft <= 0) {
      clearInterval(timer);
      timer = null;
      alert("Time's Up!");
      timeLeft = duration; // ✅ 自动重置
      updateDisplay();
      currentState = "Start";
      updateControlButton();
      accumulatedTime += Math.floor((Date.now() - startTimestamp) / 1000);
      sendTimeToServer(); // 将 totalTime 发送到后端
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
  accumulatedTime += Math.floor((Date.now() - startTimestamp) / 1000);
  sendTimeToServer();
}

function resumeTimer() {
  startTimer();
  currentState = "Pause";
  updateControlButton();
}

function resetTimer() {
  clearInterval(timer);
  timer = null;
  timeLeft = duration;
  currentState = "Start";
  updateDisplay();
  updateControlButton();
  accumulatedTime += Math.floor((Date.now() - startTimestamp) / 1000);
}

function updateControlButton() {
  const btn = document.getElementById("control-btn");
  if (currentState === "Start") {
    btn.textContent = "Start";
  } else if (currentState === "Pause") {
    btn.textContent = "Pause";
  } else if (currentState === "Resume") {
    btn.textContent = "Resume";
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
  }
  updateControlButton();
}

function sendTimeToServer() {
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch("/update_focus_time/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      tag_id: selectedTagId,
      seconds: accumulatedTime,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("Time saved", data);
      accumulatedTime = 0;
    });
}

document.addEventListener("DOMContentLoaded", () => {
  updateDisplay();
  updateControlButton();

  document
    .getElementById("control-btn")
    .addEventListener("click", handleControlClick);
  document.getElementById("reset-btn").addEventListener("click", resetTimer);
});
