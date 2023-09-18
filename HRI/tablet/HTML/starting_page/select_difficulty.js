async function read_num_game_info() {
    const api_client = new ApiClient(URL_BASE)

    var queryParams = [
        ["req", GET_JSON],
        ["json_path", "./data/registered_users.json"]
    ]
    let registered_users;
    await api_client.get('/planner', queryParams)
        .then(data => {
            registered_users = data.response;
        })
        .catch(error => console.error(error));
    queryParams = [
        ["req", GET_JSON],
        ["json_path", "./data/actual_user.json"]
    ]
    let actual_user;
    await api_client.get('/planner', queryParams)
        .then(data => {
            actual_user = data.response.user;
        })
        .catch(error => console.error(error));
    var user_game_info = registered_users[actual_user]
    var n_easy = user_game_info.Games.easy.num_games_won
    var n_medium = user_game_info.Games.medium.num_games_won
    var n_hard = user_game_info.Games.hard.num_games_won

    document.getElementById("easy").textContent = "Total win: " + n_easy
    document.getElementById("medium").textContent = "Total win: " + n_medium
    document.getElementById("hard").textContent = "Total win: " + n_hard
    console.log(n_easy, n_medium, n_hard)
}

read_num_game_info()