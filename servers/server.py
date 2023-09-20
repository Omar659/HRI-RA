from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os
import sys

# To import servers
from server_planner import Server_planner
from server_chat import Server_chat
from server_user import Server_user

# Remove log print
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Use lacal host server
app = Flask(__name__)
CORS(app)

# Different type of servers
api = Api(app)
api.add_resource(Server_planner, "/planner")
api.add_resource(Server_chat, "/chat")
api.add_resource(Server_user, "/user")

if __name__ == '__main__':
    os.system('clear')
    # Database
    print("Starting api...")
    app.run(host="0.0.0.0", port="8080")
