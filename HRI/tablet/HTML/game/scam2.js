var tiles;
var bx;
var by;
var difficult;
var image_name;
var record_moves;
var record_time;
var rows;
var cols;
var pad_l;
var pad_r;
var pad_t;
var pad_b;
var img_src;
var tiles_dim;
var grid_gap;
var game_box;
var title;
var time_record;
var moves_record;
var timer_game;
var seconds;
var minutes;
var timer;
var moves_counter;

// da riempire con json
const jsonContent = {
    "image_name": "./../images/tiles/tiles_1b.png",
    // "image_name": "empty",
    "difficult": "easy"
};
tiles = [
    ["5", "0", "4"], 
    ["1", "-", "7"],
    ["3", "2", "6"]
];
bx = 1;
by = 1;
// tiles = [
//     ["0", "1", "2"], 
//     ["3", "4", "5"],
//     ["6", "-", "7"]
// ];
// bx = 2;
// by = 1;
// tiles = [
//     ["0", "7", "-", "10"], 
//     ["8", "1", "6", "3"],
//     ["5", "4", "2", "9"]
// ];
// bx = 0;
// by = 2;
// tiles = [
//     ["0", "1", "2", "3"], 
//     ["-", "4", "10", "6"],
//     ["9", "5", "14", "7"],
//     ["8", "12", "13", "11"]
// ];
// bx = 1;
// by = 0;
difficult = jsonContent.difficult;
image_name = jsonContent.image_name;
if (image_name == "empty") {
    image_name = "./../images/tiles/tiles_default.png"
}
record_moves = "37";
record_time = "05:23";
// da riempire con json



if (difficult == "easy"){
    rows = 3;
    cols = 3;
    pad_l = "19px";
    pad_r = "27px";
    pad_t = "19px";
    pad_b = "27px";
    img_src = "./../images/backgrounds/easy_hard_slide_tile_background.png";
} else if (difficult == "medium"){
    rows = 3;
    cols = 4;
    pad_l = "23px";
    pad_r = "37px";
    pad_t = "18px";
    pad_b = "27px";
    img_src = "./../images/backgrounds/medium_slide_tile_background.png";
} else {
    rows = 4;
    cols = 4;
    pad_l = "24px";
    pad_r = "36px";
    pad_t = "24px";
    pad_b = "36px";
    img_src = "./../images/backgrounds/easy_hard_slide_tile_background.png";
}
// For image resize
tiles_dim = 80;
grid_gap = 1;

// Goal
goal_tiles = [];
cont = 0
for (let i = 0; i < rows; i++) {
    var row = []
    for (let j = 0; j < cols; j++) {
        if (i == rows-1 && j == cols-1) {
            row.push("-")
        } else {
            row.push(cont.toString())
        }
        cont++
    }
    goal_tiles.push(row)
}

// Background of game set
game_box = document.querySelector('.game_box');
game_box.style.backgroundImage = "url(" + img_src + ")";
game_box.style.setProperty('--rows', rows);
game_box.style.setProperty('--cols', cols);
game_box.style.padding = pad_t + " " + pad_r + " " + pad_b + " " + pad_l ;

// Title set
title = document.querySelector('.text-center');
title.innerHTML = '<h1 class="title">Slide game - ' + difficult.toLocaleUpperCase() + '</h1>';

// Record set
time_record = document.getElementById('timer-record');
time_record.innerHTML = "Time: " + record_time;
moves_record = document.getElementById('moves-record');
moves_record.innerHTML = "Moves: " + record_moves;

// Timer
timer_game = document.getElementById('timer-game');
seconds = 0;
minutes = 0;
timer = setInterval(update_timer, 1000);

moves_counter = 0

function is_goal(my_configuration, goal) {
    if (
        my_configuration.length !== goal.length || 
        my_configuration[0].length !== goal[0].length) {
        return false;
    }

    for (let i = 0; i < my_configuration.length; i++) {
        for (let j = 0; j < my_configuration[i].length; j++) {
            if (my_configuration[i][j] !== goal[i][j]) {
                return false;
            }
        }
    }
    return true;
}

function update_timer() {
    seconds++;
    if (seconds === 60) {
        seconds = 0;
        minutes++;
    }
    const formattedSeconds = String(seconds).padStart(2, '0');
    const formattedMinutes = String(minutes).padStart(2, '0');
    timer_game.textContent = `Time: ${formattedMinutes}:${formattedSeconds}`;
}

function update_tiles(i, j) {
    // qui probabilmente devo salvare le mie mosse
    tmp = tiles[i][j];
    tiles[i][j] = "-";
    tiles[bx][by] = tmp;
    bx = i;
    by = j;
    game_box.innerHTML = '';
    moves_counter++;
    init_game();
}

function init_game() {
    var moves_record = document.getElementById('moves-game');
    moves_record.innerHTML = "Moves: " + moves_counter;
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            const tile = document.createElement('div');
            var tile_value = tiles[i][j];
            if (tile_value == "-"){
                tile.classList.add('empty-cell');
            } else {
                tile.classList.add('cell');
                tile.textContent = tile_value;
                tile.style.background = "url(" + image_name + ")";
                const y_size = rows*tiles_dim;
                const x_size = cols*tiles_dim;
                const i_img = Math.floor(tile_value/cols);
                const j_img = tile_value%cols;
                const x_pos = -(tiles_dim-5)*j_img;
                const y_pos = -(tiles_dim-5)*i_img;
                tile.style.backgroundPositionX = x_pos + "px";
                tile.style.backgroundPositionY = y_pos + "px";
                tile.style.backgroundSize = x_size + "px " + y_size + "px";
                if (
                    (((i == bx-1 || i == bx+1) && j == by) || 
                     ((j == by-1 || j == by+1) && i == bx)) &&
                     !is_goal(tiles, goal_tiles)
                ) {
                    tile.style.cursor = "pointer"
                    tile.style.borderBottom = "3px solid #8AEB4F"
                    tile.style.borderRight = "3px solid #8AEB4F"
                    tile.style.borderLeft = "1px solid #8AEB4F"
                    tile.style.borderTop = "1px solid #8AEB4F"
                    tile.addEventListener('click', function() {
                        update_tiles(i, j);
                    });
                }
            }
            game_box.appendChild(tile);
        }
    };
    if (is_goal(tiles, goal_tiles)) {
        clearInterval(timer);
    }
    // forse da cancellare
    var cell = document.querySelector('.cell');
    cell.style.setProperty('--rows', rows);
    cell.style.setProperty('--cols', cols);
    // forse da cancellare
}

function main() {
    init_game()
}

main()