from flask import Flask

app = Flask('')

@app.route('/left')
def left():
    return "left"

@app.route('/right')
def right():
    return {"move":"right", "altro":3}

def run():
  app.run(host='0.0.0.0',port=8080)

run()