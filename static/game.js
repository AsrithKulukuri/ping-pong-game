const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth * 0.95;
canvas.height = window.innerHeight * 0.7;

const paddle = { width: 100, height: 15, x: canvas.width / 2 - 50, y: canvas.height - 30 };
const ball = { x: canvas.width / 2, y: canvas.height / 2, radius: 10, dx: 4, dy: -4 };
let score = 0;

const difficultyMap = {
    easy: 4,
    medium: 6,
    hard: 8
};

ball.dx = difficultyMap[difficulty] || 4;
ball.dy = -(difficultyMap[difficulty] || 4);

function drawPaddle() {
    ctx.fillStyle = "white";
    ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = "white";
    ctx.fill();
    ctx.closePath();
}

function drawScore() {
    ctx.fillStyle = "white";
    ctx.font = "20px Arial";
    ctx.fillText("Score: " + score, 10, 30);
}

function update() {
    ball.x += ball.dx;
    ball.y += ball.dy;

    // Wall collisions
    if (ball.x + ball.radius > canvas.width || ball.x - ball.radius < 0) {
        ball.dx = -ball.dx;
        vibrate();
    }

    if (ball.y - ball.radius < 0) {
        ball.dy = -ball.dy;
        vibrate();
    }

    // Paddle collision
    if (
        ball.y + ball.radius > paddle.y &&
        ball.x > paddle.x &&
        ball.x < paddle.x + paddle.width
    ) {
        ball.dy = -ball.dy;
        score++;
        vibrate();
    }

    // Missed paddle
    if (ball.y + ball.radius > canvas.height) {
        submitScoreAndRedirect();
        return;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawPaddle();
    drawBall();
    drawScore();
    requestAnimationFrame(update);
}

function vibrate() {
    if ("vibrate" in navigator) {
        navigator.vibrate(100);
    }
}

canvas.addEventListener("touchmove", function (e) {
    const touch = e.touches[0];
    paddle.x = touch.clientX - paddle.width / 2;
});

update();

function submitScoreAndRedirect() {
    fetch("/submit_score", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: playerName, score })
    }).then(() => {
        window.location.href = "/leaderboard";
    });
}
