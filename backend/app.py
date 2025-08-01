from flask import Flask, render_template, request, jsonify
import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

SCORES_FILE = os.path.join(BASE_DIR, "scores.json")


def load_scores():
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w') as f:
            json.dump([], f)
    with open(SCORES_FILE, 'r') as f:
        return json.load(f)


def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game")
def game():
    return render_template("game.html")


@app.route("/leaderboard")
def leaderboard():
    scores = load_scores()
    sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    return render_template("leaderboard.html", scores=sorted_scores)


@app.route("/submit_score", methods=["POST"])
def submit_score():
    data = request.get_json()
    name = data.get("name")
    score = data.get("score")
    if not name or not isinstance(score, int):
        return jsonify({"error": "Invalid data"}), 400
    scores = load_scores()
    scores.append({"name": name, "score": score})
    save_scores(scores)
    return jsonify({"message": "Score submitted!"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
