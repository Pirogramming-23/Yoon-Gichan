
let timer = null;
let elapsedHundredths = 0;
const timerDisplay = document.getElementById('timer-display');
const recordList = document.getElementById('record-list');
let countdownTimer = null;
let remainingTimeMs = 0;

// 타이머 숫자 표시 함수
function updateDisplay() {
    const seconds = String(Math.floor(elapsedHundredths / 100)).padStart(2, '0');
    const hundredths = String(elapsedHundredths % 100).padStart(2, '0');
    timerDisplay.textContent = `${seconds}:${hundredths}`;
}

// 타이머 시작 함수
function startTimer() {
if (timer !== null) return;
timer = setInterval(() => {
    elapsedHundredths++;
    updateDisplay();
}, 10);
}

// 타이머 정지 함수
function stopTimer() {
if (timer !== null) {
    clearInterval(timer);
    timer = null;
    addRecord();
}
}

// 기록 추가 함수
function addRecord() {
    const li = document.createElement('li');
    li.className = 'record-item';

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';

    const timeSpan = document.createElement('span');
    timeSpan.className = 'record-time';
    timeSpan.textContent = timerDisplay.textContent;

    li.appendChild(checkbox);
    li.appendChild(timeSpan);
    recordList.appendChild(li);
}

// 타이머 리셋
function resetTimer() {
clearInterval(timer);
timer = null;
elapsedHundredths = 0;
updateDisplay();
}

// 전체선택 함수
function toggleSelectAll() {
const checkboxes = recordList.querySelectorAll('input[type="checkbox"]');
const allChecked = Array.from(checkboxes).every(cb => cb.checked);
checkboxes.forEach(cb => cb.checked = !allChecked);
}

// 선택된 기록 삭제함수
function deleteSelected() {
const checkboxes = recordList.querySelectorAll('input[type="checkbox"]');
checkboxes.forEach(cb => {
    if (cb.checked) cb.parentElement.remove();
});
}

// 타이머 화면으로 전환
function showTimer() {
  document.getElementById('stopwatch').style.display = 'none';
  document.getElementById('timer').style.display = 'block';
}

// 스톱워치 화면으로 복귀
function showStopwatch() {
  document.getElementById('timer').style.display = 'none';
  document.getElementById('stopwatch').style.display = 'block';
}

// 타이머 시작 함수
function startCountdown() {
  const minutes = parseInt(document.getElementById('minutes-input').value, 10) || 0;
  const seconds = parseInt(document.getElementById('seconds-input').value, 10) || 0;
  remainingTimeMs = (minutes * 60 + seconds) * 1000;

  if (remainingTimeMs <= 0 || countdownTimer !== null) return;

  updateCountdownDisplay(remainingTimeMs);

  countdownTimer = setInterval(() => {
    remainingTimeMs -= 10;
    if (remainingTimeMs <= 0) {
      remainingTimeMs = 0;
      clearInterval(countdownTimer);
      countdownTimer = null;
    }
    updateCountdownDisplay(remainingTimeMs);
  }, 10);
}

// 타이머 정지 함수
function stopCountdown() {
  if (countdownTimer !== null) {
    clearInterval(countdownTimer);
    countdownTimer = null;
  }
}

// 타이머 리셋 함수
function resetCountdown() {
  stopCountdown();
  remainingTimeMs = 0;
  updateCountdownDisplay(remainingTimeMs);
  document.getElementById('minutes-input').value = 0;
  document.getElementById('seconds-input').value = 0;
}

// 타이머 화면 시간 표시 함수
function updateCountdownDisplay(remainingMs) {
  const totalSeconds = Math.floor(remainingMs / 1000);
  const hundredths = Math.floor((remainingMs % 1000) / 10);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const minutesStr = String(minutes).padStart(2, '0');
  const secondsStr = String(seconds).padStart(2, '0');
  const hundredthsStr = String(hundredths).padStart(2, '0');
  document.getElementById('countdown-display').textContent = `${minutesStr}분 ${secondsStr}초 ${hundredthsStr}`;
}