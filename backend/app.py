from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
SCORES_FILE = 'scores.json'


def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as file:
            return json.load(file)
    return []


def save_score(name, score):
    scores = load_scores()
    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:10]
    with open(SCORES_FILE, 'w') as file:
        json.dump(scores, file)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game')
def game():
    name = request.args.get('name')
    difficulty = request.args.get('difficulty')
    if not name or not difficulty:
        return redirect(url_for('index'))
    return render_template('game.html', name=name, difficulty=difficulty)


@app.route('/leaderboard')
def leaderboard():
    scores = load_scores()
    return render_template('leaderboard.html', scores=scores)


@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    name = data.get('name')
    score = data.get('score')
    if name and score is not None:
        save_score(name, score)
        return jsonify({'success': True})
    return jsonify({'success': False})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
