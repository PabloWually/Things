/*
  Order: right, up, left, down
*/
const robDx = [0, -1, 0, 1];
const robDy = [1, 0, -1, 0];

const n = 7;
const cellSize = 50;
/*
  0: blocked
  1: not blocked
*/
const maze = [
  [[1,0,0,1],[0,0,1,1],[1,0,0,1],[0,1,1,0],[1,0,0,0],[1,0,1,0],[0,0,1,1]],
  [[0,1,0,0],[0,1,0,1],[0,1,0,1],[1,0,0,1],[0,0,1,1],[0,0,0,1],[0,1,0,1]],
  [[1,0,0,1],[0,1,1,0],[1,1,0,0],[0,1,1,0],[0,1,0,1],[1,1,0,1],[0,1,1,1]],
  [[0,1,0,1],[1,0,0,1],[1,0,1,0],[0,0,1,1],[1,1,0,0],[0,1,1,0],[0,1,0,1]],
  [[1,1,0,0],[0,1,1,0],[1,0,0,1],[0,1,1,1],[1,0,0,0],[0,0,1,1],[0,1,0,1]],
  [[1,0,0,1],[1,0,1,0],[0,1,1,0],[0,1,0,1],[1,0,0,1],[0,1,1,1],[0,1,0,1]],
  [[1,1,0,0],[1,0,1,0],[0,0,1,0],[1,1,0,1],[0,1,1,0],[1,1,0,0],[0,1,1,0]]
];
const exit = [-1, 3];

let canvas, ctx;
let width, height;
let initMazeX, initMazeY;
let state = [{
  row: 7,
  col: 3,
  dir: 1
}];
let gameOver = false;
let instructionsDiv;
let treasure;
const robImagesStrings = ['right', 'back', 'left', 'front'];
let robImages = [];

let dashLen, dashOffset, dashSpeed, winX, winY, winI, winTxt;

function startAnimating() {
  canvas = document.getElementById('game');
  canvas.width = canvas.parentElement.clientWidth;
  width = canvas.width;
  height = canvas.height;
  ctx = canvas.getContext('2d');
  instructionsDiv = document.getElementById('instructions');

  treasure = new Image();
  treasure.src = './img/pirate_treasure.ico';

  robImagesStrings.forEach((src) => {
    let img = new Image();
    img.src = `./img/${src}.png`;
    robImages.push(img);
  });

  initMazeX = (width / 2 - cellSize * n / 2) + cellSize / 2;
  initMazeY = (height / 2 - cellSize * n / 2) + cellSize / 2;

  dashLen = 220;
  dashOffset = dashLen;
  dashSpeed = 5;
  winTxt = '¡GANASTE!';
  winX = initMazeX;
  winY = height / 2;
  winI = 0;

  game();
}

function game() {
  ctx.clearRect(0, 0, width, height);
  if (!gameOver) {
    let x = initMazeX, y = initMazeY;

    for (let i = 0; i < n; i++) {
      x = initMazeX;
      for (let j = 0; j < n; j++) {
        drawCell(x, y, i, j);
        x += cellSize;
      }
      y += cellSize;
    }

    let [exitRow, exitCol] = exit;
    let [exitX, exitY] = indexToScreen(exitRow, exitCol);
    exitX -= cellSize / 2;
    exitY -= cellSize / 2;
    ctx.drawImage(treasure, exitX, exitY, cellSize, cellSize);

    let {row, col, dir} = state[state.length - 1];
    drawRobot(...indexToScreen(row, col), dir);

    if (row === exitRow && col === exitCol)
      gameOver = true;

    requestAnimationFrame(game);
  } else {
    ctx.font = `50px 'Architects Daughter', cursive`;
    ctx.lineWidth = 5;
    ctx.lineJoin = 'round';
    ctx.globalAlpha = 2 / 3;
    ctx.strokeStyle = 'rgb(144, 20, 106)';
    ctx.fillStyle = 'rgb(212, 0, 114)';

    document.getElementById('btn-left').className += ' disabled';
    document.getElementById('btn-forward').className += ' disabled';
    document.getElementById('btn-right').className += ' disabled';
    document.getElementById('btn-undo').className += ' disabled';

    setTimeout(win, 2000);
  }
}

/*
  http://stackoverflow.com/questions/29911143/how-can-i-animate-the-drawing-of-text-on-a-web-page
*/
function win() {
  ctx.clearRect(winX - 2.5, 0, 120, 300);
  ctx.setLineDash([dashLen - dashOffset, dashOffset - dashSpeed]);
  dashOffset -= dashSpeed;
  ctx.strokeText(winTxt[winI], winX, winY);

  if (dashOffset > 0) {
    requestAnimationFrame(win);
  } else {
    ctx.fillText(winTxt[winI], winX, winY);
    dashOffset = dashLen;
    winX += ctx.measureText(winTxt[winI++]).width + ctx.lineWidth;
    ctx.setTransform(1, 0, 0, 1, 0, 3 * Math.random());
    ctx.rotate(Math.random() * 0.005);
    if (winI < winTxt.length)
      requestAnimationFrame(win);
  }
}

function indexToScreen(i, j) {
  let x = initMazeX, y = initMazeY;
  x += j * cellSize;
  y += i * cellSize;
  return [x, y];
}

function drawCell(x, y, i, j) {
  let cell = maze[i][j];
  let c = cellSize / 2;
  ctx.lineWidth = 5;

  let moveTo = [[x + c, y - c], [x - c, y - c], [x - c, y + c], [x + c, y + c]];
  let lineTo = [[x + c, y + c], [x + c, y - c], [x - c, y - c], [x - c, y + c]];

  for (let k = 0; k < 4; k++) {
    if (!cell[k]) {
      ctx.beginPath();
      ctx.moveTo(...moveTo[k]);
      ctx.lineTo(...lineTo[k]);
      ctx.strokeStyle = 'rgb(131, 3, 128)';
      ctx.stroke();
    }
  }
}

function drawRobot(x, y, dir, useImages = true) {
  if (useImages) {
    const size = 0.9 * cellSize;
    ctx.drawImage(robImages[dir], x - size / 2, y - size / 2, size, size);
  } else {
    const radius = 0.75 * cellSize / 2;
    let out = -5000;

    // Antennas
    ctx.fillStyle = 'black';
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 1;
    let dx1 = [out, -0.3, 0, 0.3];
    let dy1 = [out, -1.4, -1.4, -1.4];
    let dx2 = [0, 0.3, out, -0.3];
    let dy2 = [-1.4, -1.4, out, -1.4];

    ctx.beginPath();
    ctx.arc(x + dx1[dir] * radius, y + dy1[dir] * radius, radius * 0.15, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(x + dx2[dir] * radius, y + dy2[dir] * radius, radius * 0.15, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();

    ctx.beginPath();
    if (dx1[dir] !== out && dy1[dir] !== out) {
      ctx.moveTo(x, y);
      ctx.lineTo(x + dx1[dir] * radius, y + dy1[dir] * radius);
    }
    if (dx2[dir] !== out && dy2[dir] !== out) {
      ctx.moveTo(x, y);
      ctx.lineTo(x + dx2[dir] * radius, y + dy2[dir] * radius);
    }
    ctx.stroke();

    // Exterior
    ctx.fillStyle = 'white';
    ctx.strokeStyle = 'black';

    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.stroke();

    // Eyes
    ctx.fillStyle = 'rgb(212, 0, 114)';
    dx1 = [out, out, -0.9, 0.3];
    dy1 = [out, out, 0, 0];
    dx2 = [0.9, out, out, -0.3];
    dy2 = [0, out, out, 0];

    ctx.beginPath();
    ctx.arc(x + dx1[dir] * radius, y + dy1[dir] * radius, radius * 0.2, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(x + dx2[dir] * radius, y + dy2[dir] * radius, radius * 0.2, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
  }
}

function rotateLeft() {
  if (state.length > 1) {
    let {row, col, dir} = state[state.length - 1];
    dir = (dir + 1) % 4;
    state.push({row, col, dir});
    addInstruction('left');
  }
}

function advance() {
  let {row, col, dir} = state[state.length - 1];
  if (state.length === 1 || maze[row][col][dir]) {
    let {row, col, dir} = state[state.length - 1];
    row += robDx[dir];
    col += robDy[dir];
    state.push({row, col, dir});
    addInstruction('forward');
  }
}

function rotateRight() {
  if (state.length > 1) {
    let {row, col, dir} = state[state.length - 1];
    dir = (dir - 1 + 4) % 4;
    state.push({row, col, dir});
    addInstruction('right');
  }
}

function undo() {
  if (state.length > 1) {
    state.pop();
    instructionsDiv.removeChild(instructionsDiv.lastChild);
  }
}

function addInstruction(inst) {
  let message, color;
  switch (inst) {
    case 'right':
      message = 'Girar a la derecha';
      color = 'blue lighten-3 black-text';
      break;
    case 'forward':
      message = 'Avanzar';
      color = 'green darken-3';
      break;
    case 'left':
      message = 'Girar a la izquierda';
      color = 'yellow darken-4 black-text';
    break;
  }

  let chip = document.createElement('div');
  chip.className = `chip ${color}`;
  let text = document.createTextNode(message);
  chip.appendChild(text);
  instructionsDiv.appendChild(chip);
}

startAnimating();
