let lives = 4;
let firstCard = null;
let secondCard = null;
let lockBoard = false;
let matches = 0;

document.addEventListener('DOMContentLoaded', initGame);

async function initGame() {
    const board = document.getElementById('game-board');
    board.innerHTML = '<p class="loading">Cargando cartas...</p>';
    lives = 4;
    matches = 0;
    updateLives();
    resetBoard();

    try {
        const res = await fetch('/api/cartas');
        const cards = await res.json();
        renderBoard(cards);
    } catch (e) {
        console.error(e);
        board.innerHTML = "<p style='color:white'>Error de conexión</p>";
    }
}

function renderBoard(cards) {
    const board = document.getElementById('game-board');
    board.innerHTML = '';
    
    cards.forEach(c => {
        const div = document.createElement('div');
        div.className = 'card';
        div.dataset.id = c.id;
        div.dataset.matchId = c.match_id;
        div.dataset.type = c.type; // 'pair', 'true', 'false'
        
        div.innerHTML = `<div class="card-text">${c.txt}</div>`;
        div.addEventListener('click', () => handleCardClick(div));
        board.appendChild(div);
    });
}

function handleCardClick(card) {
    if (lockBoard) return;
    if (card.classList.contains('matched')) return;
    if (card === firstCard) return;

    // Sonido click opcional o efecto visual
    card.classList.add('selected');

    if (!firstCard) {
        firstCard = card;
        return;
    }

    // SEGUNDA CARTA CLICKEADA (Intento de emparejar par)
    secondCard = card;
    checkForMatch();
}

// 1. LÓGICA PARA PARES (Carta vs Carta)
function checkForMatch() {
    lockBoard = true;
    
    // Si ambas son de tipo 'pair', comprobamos si coinciden
    if (firstCard.dataset.type === 'pair' && secondCard.dataset.type === 'pair') {
        const isMatch = firstCard.dataset.matchId === secondCard.dataset.matchId;
        isMatch ? disableCards() : unflipCards();
    } else {
        // Si intentas unir una carta V/F con otra cosa -> Error
        showFeedback("¡No puedes unir estas cartas!", "red");
        unflipCards();
    }
}

// 2. LÓGICA PARA BOTONES (Verdadero/Falso)
function checkTF(userChoice) {
    // Solo funciona si hay 1 carta seleccionada y ninguna segunda carta
    if (!firstCard || secondCard) {
        showFeedback("Selecciona solo 1 carta.", "red");
        return;
    }
    
    const correctType = firstCard.dataset.type; // 'true', 'false', o 'pair'

    // Si la carta seleccionada es de un PAR, no se usa con botones
    if (correctType === 'pair') {
        showFeedback("¡Esta carta necesita pareja!", "red");
        punish();
        return;
    }

    // Comprobamos la respuesta
    if (correctType === userChoice) {
        showFeedback("¡Correcto!", "green");
        firstCard.classList.remove('selected');
        firstCard.classList.add('matched');
        
        resetBoard();
        checkWin();
    } else {
        showFeedback("¡Incorrecto!", "red");
        firstCard.classList.add('error');
        punish();
    }
}

function disableCards() {
    showFeedback("¡Pareja encontrada!", "green");
    firstCard.classList.remove('selected');
    secondCard.classList.remove('selected');
    firstCard.classList.add('matched');
    secondCard.classList.add('matched');
    resetBoard();
    checkWin();
}

function unflipCards() {
    // Esperar un poco para ver el error
    setTimeout(() => {
        firstCard.classList.add('error');
        secondCard.classList.add('error');
        punish();
    }, 200);
}

function punish() {
    lives--;
    updateLives();
    
    // Bloquear un momento para ver el rojo
    lockBoard = true; 
    setTimeout(() => {
        if (firstCard) firstCard.classList.remove('selected', 'error');
        if (secondCard) secondCard.classList.remove('selected', 'error');
        
        if (lives <= 0) {
            alert("¡GAME OVER! Se reinicia el tablero.");
            initGame();
        } else {
            resetBoard();
        }
    }, 1000);
}

function resetBoard() {
    [firstCard, secondCard] = [null, null];
    lockBoard = false;
}

function updateLives() {
    const el = document.getElementById('lives');
    el.innerText = lives;
    el.style.color = lives <= 1 ? '#ff0000' : '#ef4444';
}

function showFeedback(msg, color) {
    const el = document.getElementById('feedback-msg');
    el.innerText = msg;
    el.style.color = color === 'red' ? '#ef4444' : '#10b981';
    setTimeout(() => el.innerText = '', 1500);
}

function checkWin() {
    const remaining = document.querySelectorAll('.card:not(.matched)').length;
    if (remaining === 0) {
        setTimeout(() => alert("¡FELICIDADES! Guía completada."), 300);
    }
}