// const URL_BASE = "http://0.0.0.0:8080"
// const GET_USER = "get_user"
// const POST_SURVEY = "post_survey"

// class Slide_tile {
//     constructor(api_client) {
//         this.api_client = api_client
//     }

//     async read_game_status() {
//         const queryParams = [
//             ["req", GET_JSON],
//             ["json_path", "./data/game_status.json"]
//         ]
//         await this.api_client.get('/planner', queryParams)
//             .then(data => {
//                 this.game_status = data.response;
//             })
//             .catch(error => console.error(error));
//         console.log(this.game_status)
//         this.tiles = this.game_status.tiles;
//         this.bx = this.game_status.bx;
//         this.by = this.game_status.by
//         this.difficult = this.game_status.difficult
//         this.image_name = this.game_status.image_name
//         if (this.image_name == "empty") {
//             this.image_name = "./../images/tiles/tiles_default.png"
//         }
//         this.record_moves = this.game_status.record_moves
//         this.record_time = this.game_status.record_time
//     }

// }

async function main() {

    const api = new ApiClient(URL_BASE);
    const queryParams = [
        ["req", GET_USER],
        ["json_path", "./../../../../data/actual_user.json"]
    ]

    
    let responseData

    await api.get('/user', queryParams)
       .then(data => {responseData = data;})
       .catch(error => console.error(error));

    const name = responseData["response"]
    document.getElementById("myForm").addEventListener("submit", function (e) {
        e.preventDefault();

        
        
        var formData = new FormData(document.getElementById("myForm"));

        entries = Object.fromEntries(formData)
        // output as an object
        console.log(entries);

        var dict = {};

        // ...or iterate through the name-value pairs
        for (var pair of formData.entries()) {
            dict[pair[0]] = pair[1]
            //console.log(pair[0] + ": " + pair[1]);
        };

        const querySurvey = [
            ["req", POST_SURVEY],
            ["name", name["user"]],
            ["json_path", "./../../../../data/registered_user.json"]
            
        ];

        api.post('/user', dict, querySurvey)
            .then(data => console.log(data))
            .catch(error => console.error(error));

    });

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