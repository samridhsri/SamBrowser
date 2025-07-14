import './style.css';
import './app.css';
import '../index.css';

import logo from './assets/images/logo-universal.png';
import {Greet} from '../wailsjs/go/main/App';

document.querySelector('#app').innerHTML = `
    <img id="logo" class="logo">
      <div class="result" id="result">Please enter your name below 👇</div>
      <div class="input-box" id="input">
        <input class="input" id="name" type="text" autocomplete="off" />
        <button class="btn" onclick="greet()">Greet</button>
      </div>
    </div>
`;
document.getElementById('logo').src = logo;

let nameElement = document.getElementById("name");
nameElement.focus();
let resultElement = document.getElementById("result");

// Setup the greet function
window.greet = function () {
    // Get name
    let name = nameElement.value;

    // Check if the input is empty
    if (name === "") return;

    // Call App.Greet(name)
    try {
        Greet(name)
            .then((result) => {
                // Update result with data back from App.Greet()
                resultElement.innerText = result;
            })
            .catch((err) => {
                console.error(err);
            });
    } catch (err) {
        console.error(err);
    }
};

let time = 25 * 60;
let interval = null;

const timerDisplay = document.getElementById("timer");
const startBtn = document.getElementById("startBtn");
const resetBtn = document.getElementById("resetBtn");
const toggleBtn = document.getElementById("studyModeToggle");

function updateTimerDisplay() {
  const minutes = String(Math.floor(time / 60)).padStart(2, '0');
  const seconds = String(time % 60).padStart(2, '0');
  timerDisplay.textContent = `${minutes}:${seconds}`;
}

startBtn.onclick = () => {
  if (interval) return;
  interval = setInterval(() => {
    time--;
    updateTimerDisplay();
    if (time <= 0) {
      clearInterval(interval);
      interval = null;
    }
  }, 1000);
};

resetBtn.onclick = () => {
  clearInterval(interval);
  interval = null;
  time = 25 * 60;
  updateTimerDisplay();
};

toggleBtn.onclick = () => {
  window.backend.App.ToggleStudyMode().then((result) => {
    alert(`Study mode is now ${result ? "ON" : "OFF"}`);
  });
};

updateTimerDisplay();
