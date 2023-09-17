class Slide_tile {
    constructor(api_client) {
        this.api_client = api_client
    }

    async read_game_status() {
        const queryParams = [
            ["req", GET_JSON],
            ["json_path", "./data/game_status.json"]
        ]
        await this.api_client.get('/planner', queryParams)
            .then(data => {
                this.game_status = data.response;
            })
            .catch(error => console.error(error));
        console.log(this.game_status)
        this.tiles = this.game_status.tiles;
        this.bx = this.game_status.bx;
        this.by = this.game_status.by
        this.difficult = this.game_status.difficult
        this.image_name = this.game_status.image_name
        this.user_turn = this.game_status.user_turn
        this.plan = this.game_status.plan
        this.record_moves = this.game_status.record_moves
        this.record_time = this.game_status.record_time
    }

    init_game() {
        // Set some parameter for the board
        if (this.difficult == "easy") {
            this.rows = 3;
            this.cols = 3;
            this.pad_l = "19px";
            this.pad_r = "27px";
            this.pad_t = "19px";
            this.pad_b = "27px";
            this.img_src = "./../images/backgrounds/easy_hard_slide_tile_background.png";
        } else if (this.difficult == "medium") {
            this.rows = 3;
            this.cols = 4;
            this.pad_l = "23px";
            this.pad_r = "37px";
            this.pad_t = "18px";
            this.pad_b = "27px";
            this.img_src = "./../images/backgrounds/medium_slide_tile_background.png";
        } else {
            this.difficult = "hard"
            this.rows = 4;
            this.cols = 4;
            this.pad_l = "24px";
            this.pad_r = "36px";
            this.pad_t = "24px";
            this.pad_b = "36px";
            this.img_src = "./../images/backgrounds/easy_hard_slide_tile_background.png";
        }

        // For image resize
        this.tiles_dim = 80;
        this.grid_gap = 1;

        // Goal
        this.goal_tiles = [];
        var cont = 0
        for (let i = 0; i < this.rows; i++) {
            var row = []
            for (let j = 0; j < this.cols; j++) {
                if (i == this.rows - 1 && j == this.cols - 1) {
                    row.push("-")
                } else {
                    row.push(cont.toString())
                }
                cont++
            }
            this.goal_tiles.push(row)
        }

        // Background of game set
        this.game_box = document.querySelector('.game_box');
        this.game_box.style.backgroundImage = "url(" + this.img_src + ")";
        this.game_box.style.setProperty('--rows', this.rows);
        this.game_box.style.setProperty('--cols', this.cols);
        this.game_box.style.padding = this.pad_t + " " + this.pad_r + " " + this.pad_b + " " + this.pad_l;

        // Title set
        this.title = document.querySelector('.text-center');
        this.title.innerHTML = '<h1 class="title">Slide game - ' + this.difficult.toLocaleUpperCase() + '</h1>';

        // Record set
        this.time_record = document.getElementById('timer-record');
        this.time_record.innerHTML = "Time: " + this.record_time;
        this.moves_record = document.getElementById('moves-record');
        this.moves_record.innerHTML = "Moves: " + this.record_moves;

        // Timer
        this.seconds = 0;
        this.minutes = 0;
        this.timer_game = document.getElementById('timer-game');
        this.timer = new Timer(this);
        this.timer.start_timer();

        // Actual moves
        this.moves_counter = 0;
    }

    update_UI() {
        var moves_record = document.getElementById('moves-game');
        moves_record.innerHTML = "Moves: " + this.moves_counter;
        for (let i = 0; i < this.rows; i++) {
            for (let j = 0; j < this.cols; j++) {
                const tile = document.createElement('div');
                var tile_value = this.tiles[i][j];
                if (tile_value == "-") {
                    tile.classList.add('empty-cell');
                } else {
                    tile.classList.add('cell');
                    tile.textContent = tile_value;
                    tile.style.background = "url(" + this.image_name + ")";
                    const y_size = this.rows * this.tiles_dim;
                    const x_size = this.cols * this.tiles_dim;
                    const i_img = Math.floor(tile_value / this.cols);
                    const j_img = tile_value % this.cols;
                    const x_pos = -(this.tiles_dim - 4 - this.grid_gap) * j_img;
                    const y_pos = -(this.tiles_dim - 4 - this.grid_gap) * i_img;
                    tile.style.backgroundPositionX = x_pos + "px";
                    tile.style.backgroundPositionY = y_pos + "px";
                    tile.style.backgroundSize = x_size + "px " + y_size + "px";
                    if (
                        (((i == this.bx - 1 || i == this.bx + 1) && j == this.by) ||
                            ((j == this.by - 1 || j == this.by + 1) && i == this.bx)) &&
                        !this.is_goal()
                    ) {
                        // if 
                            tile.classList.add("clickable-cell");
                            var slide_tile = this;
                            tile.addEventListener('click', function () {
                                slide_tile.update_tiles(i, j);
                            });
                        // else
                            
                    }
                }
                this.game_box.appendChild(tile);
            }
        };
        if (this.is_goal()) {
            // setta l'ultima vittoria
            this.timer.stop_timer();
        }
    }

    update_tiles(i, j) {
        // qui probabilmente devo salvare le mie mosse
        
        // i j
        // 0 0

        // bx by
        // 0  1
        // right
        
        var tmp = this.tiles[i][j];
        this.tiles[i][j] = "-";
        this.tiles[this.bx][this.by] = tmp;
        this.bx = i;
        this.by = j;
        this.game_box.innerHTML = '';

        

        this.moves_counter++;
        // if (nmosse)
        this.update_UI();
    }

    is_goal() {
        if (
            this.tiles.length !== this.goal_tiles.length ||
            this.tiles[0].length !== this.goal_tiles[0].length) {
            return false;
        }

        for (let i = 0; i < this.tiles.length; i++) {
            for (let j = 0; j < this.tiles[i].length; j++) {
                if (this.tiles[i][j] !== this.goal_tiles[i][j]) {
                    return false;
                }
            }
        }
        return true;
    }

    toString() {
        return "" +
            "tiles: " + this.tiles + "\n" +
            "bx: " + this.bx + "\n" +
            "by: " + this.by + "\n" +
            "difficult: " + this.difficult + "\n" +
            "image_name: " + this.image_name + "\n" +
            "record_moves: " + this.record_moves + "\n" +
            "record_time: " + this.record_time + "\n" +
            "rows: " + this.rows + "\n" +
            "cols: " + this.cols + "\n" +
            "pad_l: " + this.pad_l + "\n" +
            "pad_r: " + this.pad_r + "\n" +
            "pad_t: " + this.pad_t + "\n" +
            "pad_b: " + this.pad_b + "\n" +
            "img_src: " + this.img_src + "\n" +
            "tiles_dim: " + this.tiles_dim + "\n" +
            "grid_gap: " + this.grid_gap + "\n" +
            "game_box: " + this.game_box + "\n" +
            "title: " + this.title + "\n" +
            "time_record: " + this.time_record + "\n" +
            "moves_record: " + this.moves_record + "\n" +
            "seconds: " + this.seconds + "\n" +
            "minutes: " + this.minutes + "\n" +
            "timer: " + this.timer.toString() + "\n" +
            "moves_counter: " + this.moves_counter
    }
}

async function main() {

    const api = new ApiClient(URL_BASE);
    var slide_tile = new Slide_tile(api)
    await slide_tile.read_game_status()

    slide_tile.init_game()

    slide_tile.update_UI()

    console.log(slide_tile.toString())
    
    // listener {
    //     leggi il File
    //     se è true
    //         aggiorna variabile
    //         update_UI
    // }
    // const queryParams = [
    //     ["req", GET_JSON],
    //     ["json_path", "./data/game_status.json"]
    // ]

    // api.get('/planner', queryParams)
    //     .then(data => console.log(data))
    //     .catch(error => console.error(error));
}

main()