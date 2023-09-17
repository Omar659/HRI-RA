async function go_to_game() {
    const queryParams = [
          ["req", GET_JSON],
          ["json_path", "./data/game_status.json"]
      ]
      await this.api_client.get('/planner', queryParams)
          .then(data => {
              this.game_status = data.response;
          })
          .catch(error => console.error(error));
    window.location.href = './../game/game.html'
  }