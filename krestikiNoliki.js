const board = document.querySelector('.value');
let count = 0;


board.addEventListener("click", function(e) {
  if (e.target.className=="slot") {
    if (e.value = '' & count%2 == 0){
        e.target.innerHTML = 'X';
        count += 1;
    } else if (e.target.value = '' & count%2 != 0){
        e.target.innerHTML = '0';
        count += 1;
    };
        
    
  };
});
