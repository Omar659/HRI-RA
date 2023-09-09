from flask import Flask

app = Flask('')

@app.route('/left')
def left():
    return "left"

@app.route('/chat')
def chat():
    nome = input("Dimmi il tuo nome: ")
    return {"move": [1, 3], "nome": nome}

def run():
  app.run(host='0.0.0.0',port=8081)

run()