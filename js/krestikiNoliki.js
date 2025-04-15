const board = document.querySelector('.value');
let count = 0;


board.addEventListener("click", function(e) {
  if (e.target.className=="slot") {
    if (e.target.textContent == '' & count%2 == 0){
        e.target.innerHTML = 'X';
        count += 1;
    } else if (e.target.textContent == '' & count%2 != 0){
        e.target.innerHTML = '0';
        count += 1;
    };
  };
  chek()
});



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