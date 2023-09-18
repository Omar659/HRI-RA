class Tutorial {
    constructor(api_client) {
        this.api_client = api_client
    }

    init_game() {
        // Set some parameter for the board
        this.rows = 3;
        this.cols = 3;

        // For image resize
        this.tiles_dim = 80;
        this.grid_gap = 1;

        // Background of game set
        this.game_box = document.querySelector('.game_box');
        this.game_box.style.setProperty('--rows', this.rows);
        this.game_box.style.setProperty('--cols', this.cols);

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
        this.game_box.innerHTML = '';
        for (let i = 0; i < 9; i++) {
            var tile = document.createElement('div');
            tile.id = "c" + i.toString()
            this.game_box.appendChild(tile);
        }

        var moves = document.getElementById("moves-game");
        moves.textContent = "Moves: " + this.moves_counter.toString()
        var tutorial = this
        if (this.moves_counter == 0) {
            var c0 = document.getElementById('c0');
            c0.textContent = "0";
            c0.classList.add("clickable-cell")
            c0.addEventListener('click', function () {
                alert("sbagliato")
            });

            var c1 = document.getElementById('c1');
            c1.textContent = "1";
            c1.classList.add("cell")

            var c2 = document.getElementById('c2');
            c2.textContent = "2";
            c2.classList.add("cell")

            var c3 = document.getElementById('c3');
            c3.classList.add("empty-cell")

            var c4 = document.getElementById('c4');
            c4.textContent = "4";
            c4.classList.add("clickable-cell")
            c4.addEventListener('click', function () {
                alert("sbagliato")
            });

            var c5 = document.getElementById('c5');
            c5.textContent = "5";
            c5.classList.add("cell")

            var c6 = document.getElementById('c6');
            c6.textContent = "3";
            c6.classList.add("clickable-cell")
            c6.addEventListener('click', function () {
                tutorial.moves_counter++;
                tutorial.update_UI()
            });

            var c7 = document.getElementById('c7');
            c7.textContent = "6";
            c7.classList.add("cell")

            var c8 = document.getElementById('c8');
            c8.textContent = "7";
            c8.classList.add("cell")
        }
        if (this.moves_counter == 1) {
            var c0 = document.getElementById('c0');
            c0.textContent = "0";
            c0.classList.add("cell")

            var c1 = document.getElementById('c1');
            c1.textContent = "1";
            c1.classList.add("cell")

            var c2 = document.getElementById('c2');
            c2.textContent = "2";
            c2.classList.add("cell")

            var c3 = document.getElementById('c3');
            c3.textContent = "3";
            c3.classList.add("clickable-cell")
            c3.addEventListener('click', function () {
                alert("sbagliato")
            });

            var c4 = document.getElementById('c4');
            c4.textContent = "4";
            c4.classList.add("cell")

            var c5 = document.getElementById('c5');
            c5.textContent = "5";
            c5.classList.add("cell")

            var c6 = document.getElementById('c6');
            c6.classList.add("empty-cell")

            var c7 = document.getElementById('c7');
            c7.textContent = "6";
            c7.classList.add("clickable-cell")
            c7.addEventListener('click', function () {
                tutorial.moves_counter++;
                tutorial.update_UI()
            });

            var c8 = document.getElementById('c8');
            c8.textContent = "7";
            c8.classList.add("cell")

        } else if (this.moves_counter == 2) {
            var c0 = document.getElementById('c0');
            c0.textContent = "0";
            c0.classList.add("cell")

            var c1 = document.getElementById('c1');
            c1.textContent = "1";
            c1.classList.add("cell")

            var c2 = document.getElementById('c2');
            c2.textContent = "2";
            c2.classList.add("cell")

            var c3 = document.getElementById('c3');
            c3.textContent = "3";
            c3.classList.add("cell")

            var c4 = document.getElementById('c4');
            c4.textContent = "4";
            c4.classList.add("clickable-cell")
            c4.addEventListener('click', function () {
                alert("sbagliato")
            });

            var c5 = document.getElementById('c5');
            c5.textContent = "5";
            c5.classList.add("cell")

            var c6 = document.getElementById('c6');
            c6.classList.add("clickable-cell")
            c6.textContent = "6"
            c6.addEventListener('click', function () {
                alert("sbagliato")
            });

            var c7 = document.getElementById('c7');
            c7.classList.add("empty-cell")

            var c8 = document.getElementById('c8');
            c8.textContent = "7";
            c8.classList.add("clickable-cell")
            c8.addEventListener('click', function () {
                tutorial.moves_counter++;
                tutorial.update_UI()
            });

        }
        if (this.moves_counter == 3) {
            var c0 = document.getElementById('c0');
            c0.textContent = "0";
            c0.classList.add("cell")

            var c1 = document.getElementById('c1');
            c1.textContent = "1";
            c1.classList.add("cell")

            var c2 = document.getElementById('c2');
            c2.textContent = "2";
            c2.classList.add("cell")

            var c3 = document.getElementById('c3');
            c3.textContent = "3";
            c3.classList.add("cell")

            var c4 = document.getElementById('c4');
            c4.textContent = "4";
            c4.classList.add("cell")

            var c5 = document.getElementById('c5');
            c5.textContent = "5";
            c5.classList.add("cell")

            var c6 = document.getElementById('c6');
            c6.textContent = "6";
            c6.classList.add("cell")

            var c7 = document.getElementById('c7');
            c7.textContent = "7";
            c7.classList.add("cell")

            var c8 = document.getElementById('c8');
            c8.classList.add("empty-cell")

            

            this.timer.stop_timer();

            document.getElementById('gg').style.visibility='visible';

            
            
        }
    }

    toString() {
        return "" +
            "rows: " + this.rows + "\n" +
            "cols: " + this.cols + "\n" +
            "tiles_dim: " + this.tiles_dim + "\n" +
            "grid_gap: " + this.grid_gap + "\n" +
            "game_box: " + this.game_box + "\n" +
            "seconds: " + this.seconds + "\n" +
            "minutes: " + this.minutes + "\n" +
            "timer: " + this.timer.toString() + "\n" +
            "moves_counter: " + this.moves_counter
    }
}



async function main() {
    const api = new ApiClient(URL_BASE);
    var tutorial = new Tutorial(api)

    tutorial.init_game()

    tutorial.update_UI()

    console.log(tutorial.toString())
}

main()
