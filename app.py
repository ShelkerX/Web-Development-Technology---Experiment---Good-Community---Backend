import os
import math
import pandas as pd

from flask import Flask, render_template, request
from flask_cors import CORS
from src.api.user_api import user
from src.api.request_api import req
from src.api.response_api import rsp
from src.api.admin_api import admin

app = Flask(__name__,
            template_folder="public",
            static_folder="public",
            static_url_path="/")

app.register_blueprint(user)
app.register_blueprint(req)
app.register_blueprint(rsp)
app.register_blueprint(admin)
CORS(app, supports_credentials=True, origins="*")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
