class Timer {
    constructor(game) {
        // Timer
        this.game = game
    }

    start_timer() {
        this.timer = setInterval(this.update_timer, 1000, this.game);
    }

    stop_timer() {
        clearInterval(this.timer);
    }

    update_timer(game) {
        game.seconds++;
        if (game.seconds === 60) {
            game.seconds = 0;
            game.minutes++;
        }
        const formattedSeconds = String(game.seconds).padStart(2, '0');
        const formattedMinutes = String(game.minutes).padStart(2, '0');
        game.timer_game.textContent = `Time: ${formattedMinutes}:${formattedSeconds}`;
    }

    toString() {
        const formattedSeconds = String(this.seconds).padStart(2, '0');
        const formattedMinutes = String(this.minutes).padStart(2, '0');
        return `Time: ${formattedMinutes}:${formattedSeconds}`
    }
}