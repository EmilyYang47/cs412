// File: time_left_counter.js
// Author: Emily Yang (eyang4@bu.edu), 6/18/2025
// Description: The time_left_counter js file which creates the countdown timer
// showing how much time is left from current time to the due time of a task description.

const dueTime = document.getElementById("due_time");
const countdownBox = document.getElementById("countdown_box");

const dueDate = Date.parse(dueTime.textContent);

// For every second, update the countdown timer
setInterval(() => {
  const now = new Date().getTime();

  const diff = dueDate - now;

  const d = Math.floor(
    dueDate / (1000 * 60 * 60 * 24) - now / (1000 * 60 * 60 * 24)
  );
  const h = Math.floor(
    (dueDate / (1000 * 60 * 60) - now / (1000 * 60 * 60)) % 24
  );
  const m = Math.floor((dueDate / (1000 * 60) - now / (1000 * 60)) % 60);
  const s = Math.floor((dueDate / 1000 - now / 1000) % 60);

  if (diff > 0) {
    countdownBox.innerHTML =
      d + "days, " + h + "hours, " + m + "minutes, " + s + "seconds";
  }
}, 1000);
