let score = 0; //점수
let hintUsed = false;
let attempts=9;
const digits = [];

window.addEventListener('DOMContentLoaded', init_game);

//입력창 초기화 함수(반복되서 따로 빼둠)
function clearInputs() {
    for (let i = 1; i <= 3; i++) {
        document.querySelector(`#number${i}`).value = '';
    }
}

function init_game() {
    // 기본변수 초기화
    attempts=9
    score = 0;
    hintUsed = false;
    const hintBtn = document.querySelector('.hint-button');
    if (hintBtn) hintBtn.disabled = false;
    const attemptsEl = document.getElementById('attempts');
    if (attemptsEl) attemptsEl.innerHTML = attempts;
    // digits 배열 초기화 및 3개의 중복없는 숫자 생성
    digits.length = 0;
    while (digits.length < 3) {
        const rand = Math.floor(Math.random() * 10);
        if (!digits.includes(rand)) digits.push(rand);
    }
    // 이전에 생성된 restart 버튼 제거
    const prevRestartBtn = document.querySelectorAll('.restart-button');
    prevRestartBtn.forEach(btn => btn.remove());
    //html의 input과 결과창 비우기
    clearInputs();
    const resultEl = document.getElementById('results');
    if (resultEl) resultEl.innerHTML = '';
    const img = document.querySelector('#game-result-img');
    img.src="";
    //다시 시작하기 버튼 눌렀을 때 다시 확인하기 버튼 활성화
    document.querySelector('.submit-button').disabled = false;
    //디버깅용
    console.log('정답 숫자:', digits);
}

function check_numbers () {
    //시도횟수 설정
    attempts -=1;
    const attemptsEl = document.getElementById('attempts');
    if (attemptsEl) attemptsEl.innerHTML = attempts;

    // 볼과 스트라이크 횟수 초기화
    let ball_count = 0;
    let strike_count = 0;

    // 시도횟수가 3일시 힌트제공
    if (!hintUsed && attempts === 3) {
        show_hint();
    }
    //입력한 숫자 개수 확인
    const checking_numbers = [];
    let allFilled = true;
    for (let i = 0; i < 3; i++) {
        const inputEl = document.querySelector(`#number${i+1}`);
        if (inputEl) {
            const value = inputEl.value;
            if (value === '') {
                allFilled = false;
            }
            checking_numbers.push(Number(value));
            inputEl.value = '';
        }
    }
    if (!allFilled || checking_numbers.includes(NaN)) {
        const resultEl = document.getElementById('results');
        if (resultEl) {
            const p = document.createElement('p');
            p.className = 'result';
            p.textContent = '숫자 3개를 전부 입력해주세요.';
            resultEl.appendChild(p);
        }
        return;
    }
    //숫자 3개 입력되었을때
    //중복 숫자 있는지 확인
    const hasDuplicates = new Set(checking_numbers).size !== checking_numbers.length;
    if (hasDuplicates) {
        const resultEl = document.getElementById('results');
        if (resultEl) {
            const p = document.createElement('p');
            p.className = 'result';
            p.textContent = '숫자 3개는 달라야 합니다.';
            resultEl.appendChild(p);
        }
        return;
    }
    //입력된 숫자들과 정답을 비교하여 볼과 스트라이크 횟수 세기
    for (let i = 0; i < 3; i++) {
        if (digits.includes(checking_numbers[i])) {
            ball_count++;
        }
        if (digits[i] === checking_numbers[i]) {
            strike_count++;
        }
    }
    ball_count -= strike_count;

    //생성된 결과에 따라 html 업데이트하기
    const resultEl = document.getElementById('results');
    let p = document.createElement('p');
    if (strike_count === 0 && ball_count === 0) {
        p.innerHTML = `${checking_numbers.join(' ')} : <span style="background-color:red; color:white; padding:4px; border-radius:50%">O</span>`;
    } else {
        p.innerHTML = `${checking_numbers.join(' ')} : ${strike_count > 0 ? strike_count + '<span style="background-color:green; color:white; padding:4px; border-radius:50%"> S</span>' : ''}${ball_count > 0 ? ball_count + '<span style="background-color:yellow; color:black; padding:4px; border-radius:50%"> B</span>' : ''}`;
    }
    if (resultEl) resultEl.appendChild(p);

    //게임 오버 여부 체크
    if(strike_count==3) { 
        const img = document.querySelector('#game-result-img');
        img.src="success.png";
        document.querySelector('.submit-button').disabled = true;
        // 게임 오버시 다시 시작하기 버튼 추가
        const restartBtn = document.createElement('button');
        restartBtn.textContent = '다시시작하기';
        restartBtn.classList.add('restart-button', 'submit-button');
        restartBtn.style.marginLeft = '10px';
        restartBtn.onclick = init_game;
        const submitBtn = document.querySelector('.submit-button');
        submitBtn.parentNode.insertBefore(restartBtn, submitBtn.nextSibling);
        //점수 제도(점수=남은시도횟수*100)
        score = attempts * 100;
        const scoreP = document.createElement('p');
        scoreP.className = 'result';
        scoreP.textContent = `점수: ${score}점`;
        resultEl.appendChild(scoreP);
    }
    else if(attempts==0){
        const img = document.querySelector('#game-result-img');
        img.src="fail.png";
        document.querySelector('.submit-button').disabled = true;
        // 게임 오버시 다시 시작하기 버튼 추가
        const restartBtn = document.createElement('button');
        restartBtn.textContent = '다시시작하기';
        restartBtn.classList.add('restart-button', 'submit-button');
        restartBtn.style.marginLeft = '10px';
        restartBtn.onclick = init_game;
        const submitBtn = document.querySelector('.submit-button');
        submitBtn.parentNode.insertBefore(restartBtn, submitBtn.nextSibling);
    }
}
//힌트 보여주는 함수
function show_hint() {
    if (hintUsed) return;
    hintUsed = true;
    const index = Math.floor(Math.random() * 3);
    const hintNumber = digits[index];
    const resultEl = document.getElementById('results');
    const hintP = document.createElement('p');
    hintP.className = 'result';
    hintP.textContent = `힌트: ${index + 1}번째 숫자는 ${hintNumber}입니다.`;
    resultEl.appendChild(hintP);
    const hintBtn = document.querySelector('.hint-button');
    if (hintBtn) hintBtn.disabled = true;
}