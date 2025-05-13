const roomCode = document.querySelector('#game').dataset.roomCode; // например, <div id="game" data-room-code="{{ room_code }}"></div>

const board = document.querySelector('.value');
let count = 0; // Можно инициализировать с сервера, если нужно

board.addEventListener("click", async function(e) {
  if (e.target.classList.contains("slot") && e.target.textContent === '') {
    const index = parseInt(e.target.dataset.num); // data-num от 0 до 8
    const playerSymbol = count % 2 === 0 ? 'X' : '0';

    try {
      const response = await fetch(`/api/room/${roomCode}/move`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ index: index, symbol: playerSymbol })
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.error || 'Ошибка при отправке хода');
        return;
      }

      const data = await response.json();
      updateBoard(data.board);
      count += 1;

      if (data.winner) {
        alert(`Победил игрок ${data.winner}`);
        // Можно заблокировать дальнейшие ходы или предложить начать новую игру
      }

    } catch (err) {
      alert('Ошибка соединения с сервером');
      console.error(err);
    }
  }
});

function updateBoard(boardArray) {
  for (let i = 0; i < 9; i++) {
    const row = Math.floor(i / 3);
    const col = i % 3;
    const cell = document.querySelector(`.slot[data-num='${i}']`);
    cell.textContent = boardArray[row][col];
  }
}



function chek(){
  cells = document.querySelectorAll('[data-num]')
  if (cells[0].textContent =='X' & cells[4].textContent=='X' & cells[8].textContent=='X' || cells[0].textContent =='0' & cells[4].textContent=='0' & cells[8].textContent=='0'){
    cells[0].style = `background:rgb(49, 234, 33)`;
    cells[4].style = `background:rgb(49, 234, 33)`;
    cells[8].style = `background:rgb(49, 234, 33)`;
  }else if(cells[2].textContent =='X' & cells[4].textContent=='X' & cells[6].textContent=='X'||cells[2].textContent =='0' & cells[4].textContent=='0' & cells[6].textContent=='0'){
    cells[2].style = `background:rgb(49, 234, 33)`;
    cells[4].style = `background:rgb(49, 234, 33)`;
    cells[6].style = `background:rgb(49, 234, 33)`;
  }else if(cells[0].textContent =='X' & cells[3].textContent=='X' & cells[6].textContent=='X'||cells[0].textContent =='0' & cells[3].textContent=='0' & cells[6].textContent=='0'){
    cells[0].style = `background:rgb(49, 234, 33)`;
    cells[3].style = `background:rgb(49, 234, 33)`;
    cells[6].style = `background:rgb(49, 234, 33)`;
  }else if(cells[1].textContent =='X' & cells[4].textContent=='X' & cells[7].textContent=='X'||cells[1].textContent =='0' & cells[4].textContent=='0' & cells[7].textContent=='0'){
    cells[1].style = `background:rgb(49, 234, 33)`;
    cells[4].style = `background:rgb(49, 234, 33)`;
    cells[7].style = `background:rgb(49, 234, 33)`;
  }else if(cells[2].textContent =='X' & cells[5].textContent=='X' & cells[8].textContent=='X'||cells[2].textContent =='0' & cells[5].textContent=='0' & cells[8].textContent=='0'){
    cells[2].style = `background:rgb(49, 234, 33)`;
    cells[5].style = `background:rgb(49, 234, 33)`;
    cells[8].style = `background:rgb(49, 234, 33)`;
  }else if(cells[0].textContent =='X' & cells[1].textContent=='X' & cells[2].textContent=='X'||cells[0].textContent =='0' & cells[1].textContent=='0' & cells[2].textContent=='0'){
    cells[0].style = `background:rgb(49, 234, 33)`;
    cells[1].style = `background:rgb(49, 234, 33)`;
    cells[2].style = `background:rgb(49, 234, 33)`;
  }else if(cells[3].textContent =='X' & cells[4].textContent=='X' & cells[5].textContent=='X'||cells[3].textContent =='0' & cells[4].textContent=='0' & cells[5].textContent=='0'){
    cells[3].style = `background:rgb(49, 234, 33)`;
    cells[4].style = `background:rgb(49, 234, 33)`;
    cells[5].style = `background:rgb(49, 234, 33)`;
  }else if(cells[6].textContent =='X' & cells[7].textContent=='X' & cells[8].textContent=='X'||cells[6].textContent =='0' & cells[7].textContent=='0' & cells[8].textContent=='0'){
    cells[6].style = `background:rgb(49, 234, 33)`;
    cells[7].style = `background:rgb(49, 234, 33)`;
    cells[8].style = `background:rgb(49, 234, 33)`;
  }
};



/*

board.addEventListener("click", function(e) {
  if (e.target.className=="slot") {
    if (e.target.value == ''){
      if(count%2 == 0){
        e.target.innerHTML = 'X';
          count += 1;
      }else if (count%2 != 0){
          e.target.innerHTML = '0';
          count += 1;
    };};  
  };
});

*/