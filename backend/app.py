from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(
    __name__,
    template_folder="../templates",  # HTML templates (index.html, etc.)
    static_folder="../static"        # Static files (JS, CSS)
)

# Path to the JSON file for storing scores
SCORES_FILE = "../scores.json"

# Load scores from file


def load_scores():
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w') as f:
            json.dump([], f)
    with open(SCORES_FILE, 'r') as f:
        return json.load(f)

# Save scores to file


def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

# Homepage


@app.route("/")
def index():
    return render_template("index.html")

# Game page


@app.route("/game")
def game():
    return render_template("game.html")

# Leaderboard


@app.route("/leaderboard")
def leaderboard():
    scores = load_scores()
    sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    return render_template("leaderboard.html", scores=sorted_scores)

# Score submission endpoint


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


# App runner
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use dynamic port for Render
    app.run(debug=False, host="0.0.0.0", port=port)
