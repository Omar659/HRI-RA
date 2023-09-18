async function go_to_game(difficulty) {
    var api = new ApiClient(URL_BASE)
    // scegli difficoltà

    var dict = {
        "difficult": difficulty
    }; // difficoltà da prendere da html


    const query = [
        ["req", POST_GAME_STATUS]
    ];

    await api.post('/planner', dict, query)
        .then(data => console.log(data))
        .catch(error => console.error(error));
    window.location.href = './../game/game.html'
}