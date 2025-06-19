console.log("Hiiii");

const dueTime = document.getElementById("due_time");
const countdownBox = document.getElementById("countdown_box");

const dueDate = Date.parse(dueTime.textContent);

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
