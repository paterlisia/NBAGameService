from flask import Flask, Response, request
from datetime import datetime
import json
from games import Game
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__)

CORS(app)


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "NBAGameService",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/api/games/<date>", methods=["GET"])
def get_games_by_date(date):
    result = Game.get_by_date(date)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

