class Slide_tile {
    constructor() {
        // var status = JSON.parse("./data/game_status.json")
        this.read_json("./data/game_status.json")
        // console.log(status)
    }

    read_json(json_path) {
        fetch(json_path)
            .then((response) => response.json())
            .then((json) => console.log(json));
    }
}

function main() {
    slide_tile = new Slide_tile()
}

main()
