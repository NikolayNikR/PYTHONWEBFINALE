const roomCode = document.querySelector('#game').dataset.roomCode;
const playerSymbol = document.querySelector('#game').dataset.playerSymbol;
const board = document.querySelector('.value');
const resetBtn = document.getElementById('reset-btn');
const info = document.getElementById('info');

let lastBoardState = null;
let gameOver = false;

function showMessage(msg) {
    info.textContent = msg;
}

resetBtn.addEventListener('click', async () => {
    try {
        const response = await fetch(`/api/room/${roomCode}/reset`, {
            method: 'POST'
        });
        if (!response.ok) throw new Error('Ошибка при сбросе игры');

        gameOver = false;
        resetBtn.style.display = 'none';
        lastBoardState = null;

        // Сброс цвета текста всех ячеек в чёрный
        document.querySelectorAll('.slot').forEach(slot => {
            slot.style.color = 'black';
            slot.classList.remove('winner'); // убираем класс подсветки, если есть
        });

        await updateBoard();
    } catch (err) {
        showMessage('Не удалось сбросить игру');
        console.error(err);
    }
});


function checkWinAndHighlight() {
    const slots = document.querySelectorAll('.slot');
    const lines = [
        [0,1,2], [3,4,5], [6,7,8], // строки
        [0,3,6], [1,4,7], [2,5,8], // столбцы
        [0,4,8], [2,4,6]           // диагонали
    ];

    // Сначала убираем подсветку
    slots.forEach(slot => slot.classList.remove('winner'));

    for (const line of lines) {
        const [a,b,c] = line;
        const valA = slots[a].textContent;
        const valB = slots[b].textContent;
        const valC = slots[c].textContent;

        if (valA !== '' && valA === valB && valB === valC) {
            // Подсвечиваем выигрышную линию
            slots[a].style.color = 'rgb(0,255,0)';
            slots[b].style.color = 'rgb(0,255,0)';
            slots[c].style.color = 'rgb(0,255,0)';
            return valA, gameOver=true; // возвращаем символ победителя
        }
    }
    return null; // победы нет
}


async function getRoom() {
    try {
        const response = await fetch(`/api/room/${roomCode}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Could not get room:", error);
        return null;
    }
}

async function updateBoard() {
    const roomData = await getRoom();

    if (!roomData) {
        console.error("Failed to update board: Could not retrieve room data.");
        return;
    }

    const boardState = roomData.board;

    if (JSON.stringify(boardState) === JSON.stringify(lastBoardState)) {
        return; // Нет изменений
    }
    if(gameOver == false){
        lastBoardState = boardState;

        document.querySelectorAll('.slot').forEach((slot, index) => {
            const row = Math.floor(index / 3);
            const col = index % 3;
            slot.textContent = boardState[row][col];
        });

        const winner = checkWinAndHighlight();
    }

    if (winner) {
        showMessage(`Победил игрок ${winner}!`);
        // Можно заблокировать доску или предложить начать новую игру
    }
}

board.addEventListener("click", async function(e) {
    if (e.target.classList.contains("slot") && e.target.textContent === '') {
        const index = parseInt(e.target.dataset.num);

        try {
            const response = await fetch(`/api/room/${roomCode}/move`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ index: index, symbol: playerSymbol })
            });

            if (!response.ok) {
                const errorData = await response.json();
                showMessage(errorData.error || 'Ошибка при отправке хода');
                return;
            }

            const data = await response.json();
            updateBoard();

            if (data.winner) {
                showMessage(`Победил игрок ${winner}!`);
                // Можно заблокировать дальнейшие ходы или предложить начать новую игру
            }

        } catch (err) {
            showMessage('Ошибка соединения с сервером');
            console.error(err);
        }
    }
});

// Запускаем обновление доски каждую секунду
setInterval(updateBoard, 1000);

// Обновляем доску сразу при загрузке страницы
updateBoard();


