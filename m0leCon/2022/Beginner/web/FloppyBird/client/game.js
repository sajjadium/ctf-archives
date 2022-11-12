let canvas;
let ctx;

document.addEventListener("DOMContentLoaded", function() {
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");
    game.load();
    setInterval(loop, 1000 / 60);
});

let background = {
    x: 0,
    y: 0,
    width: 288,
    height: 512,
    image: new Image(),
    load: function() {
        this.image.src = "images/background.png";
    },
    draw: function() {
        ctx.drawImage(this.image, this.x, this.y, this.width, this.height);
    }
};

let ground = {
    x: 0,
    y: 512 - 112,
    width: 288,
    height: 112,
    image: new Image(),
    load: function() {
        this.image.src = "images/ground.png";
    },
    draw: function() {
        ctx.drawImage(this.image, this.x, this.y, this.width, this.height);
    }
};

let bird = {
    x: 50,
    y: (background.height - ground.height) / 3,
    width: 34,
    height: 24,
    images: [
        new Image(),
        new Image(),
        new Image(),
    ],
    velocity: -5,
    state: 0,
    load: function() {
        this.images[0].src = "images/yellowbird-downflap.png";
        this.images[1].src = "images/yellowbird-midflap.png";
        this.images[2].src = "images/yellowbird-upflap.png";
    },
    draw: function() {
        ctx.drawImage(this.images[this.state], this.x, this.y, this.width, this.height);
    }
};

let pipes = {
    top: {
        x: [],
        y: [],
        width: 52,
        height: 320,
        image: new Image(),
        load: function() {
            this.image.src = "images/pipe-green.png";
        },
        draw: function() {
            for (let i = 0; i < this.x.length; i++) {
                ctx.save();
                ctx.translate(this.x[i] + this.width / 2, this.y[i] + this.height / 2);
                ctx.rotate(Math.PI);
                ctx.drawImage(this.image, -this.width / 2, -this.height / 2, this.width, this.height);
                ctx.restore();
            }
        }
    },
    bottom: {
        x: [],
        y: [],
        width: 52,
        height: 320,
        image: new Image(),
        load: function() {
            this.image.src = "images/pipe-green.png";
        },
        draw: function() {
            for (let i = 0; i < this.x.length; i++) {
                ctx.drawImage(this.image, this.x[i], this.y[i], this.width, this.height);
            }
        }
    },
};

let message = {
    x: (background.width - 184) / 2,
    y: (background.height - ground.height - 267) / 2,
    width: 184,
    height: 267,
    image: new Image(),
    load: function() {
        this.image.src = "images/message.png";
    },
    draw: function() {
        ctx.drawImage(this.image, this.x, this.y, this.width, this.height);
    }
};

let gameOver = {
    x: (background.width - 192) / 2,
    y: (background.height - ground.height - 42) / 2,
    width: 192,
    height: 42,
    image: new Image(),
    load: function() {
        this.image.src = "images/gameover.png";
    },
    draw: function() {
        ctx.drawImage(this.image, this.x, this.y, this.width, this.height);
    }
};

let game = {
    score: 0,
    state: 0,
    load: function() {
        background.load();
        ground.load();
        bird.load();
        pipes.top.load();
        pipes.bottom.load();
        message.load();
        gameOver.load();
    },
    draw: function() {
        if (this.state === 2 || this.state === 3) {
            background.draw();
            pipes.top.draw();
            pipes.bottom.draw();
            bird.draw();

            if (this.state === 3)
                gameOver.draw();
            ground.draw();
        } else {
            background.draw();
            
            if (this.state === 0)
                message.draw();
            else {
                pipes.top.draw();
                pipes.bottom.draw();
                bird.draw();
            }
            ground.draw();
        }
    },
    restart: function() {
        score.innerHTML = "FLOPPY BIRD - 0/1000";
        this.score = 0;
        this.state = 0;
        bird.velocity = -5;
        bird.y = (background.height - ground.height) / 3;
        pipes.top.x = [];
        pipes.bottom.x = [];
        pipes.top.y = [];
        pipes.bottom.y = [];
    }
};

let frame = 0;

let loop = function() {   
    game.draw();

    if (game.state === 1) {
        bird.velocity += 0.32;
        bird.y += bird.velocity

        if (bird.y < 0)
            bird.y = 0;

        if (++frame % 5 == 0)
            bird.state = (bird.state + 1) % 3;
        
        for (let i = 0; i < pipes.top.x.length; i++) {
            pipes.top.x[i] -= 2;
            pipes.bottom.x[i] -= 2;

            if (pipes.top.x[i] + pipes.top.width < 0) {
                pipes.top.x.splice(i, 1);
                pipes.bottom.x.splice(i, 1);
                pipes.top.y.splice(i, 1);
                pipes.bottom.y.splice(i, 1);
            }
        }

        if (pipes.top.x.length == 0 || pipes.top.x[pipes.top.x.length - 1] < background.width / 4) {
            pipes.top.x.push(background.width);
            pipes.bottom.x.push(background.width);
            pipes.top.y.push(-(Math.random() * (228 - 40) + 40));
            pipes.bottom.y.push(pipes.top.y[pipes.top.y.length - 1] + 100 + 320);
        }
        
        if (
            (
                (
                    bird.x + bird.width > pipes.top.x[0]
                    && bird.x < pipes.top.x[0] + pipes.top.width
                )
                && (
                    bird.y < pipes.top.y[0] + pipes.top.height
                    || bird.y + bird.height > pipes.bottom.y[0]
                )
            )
            || bird.y + bird.height > background.height - ground.height
        ) {
            game.state = 2;

            if (bird.y + bird.height > background.height - ground.height)
                bird.y = background.height - ground.height - bird.height;
        }
        else if (bird.x === pipes.top.x[0] + pipes.top.width + 2) {
            let score = document.getElementById("score");
            score.innerHTML = "FLOPPY BIRD - " + ++game.score + "/1000";
            updateScore(game.score);
        }
    } else if (game.state === 2) {
        if (
            (
                !(
                    bird.x + bird.width > pipes.top.x[0] + 2
                    && bird.x < pipes.top.x[0] + 2 + pipes.top.width
                )
                && bird.y + bird.height < background.height - ground.height
            )
            || (
                (
                    bird.x + bird.width > pipes.top.x[0] + 2
                    && bird.x < pipes.top.x[0] + 2 + pipes.top.width
                )
                && bird.y + bird.height < pipes.bottom.y[0] + 2
            )
        ) {
            if (bird.velocity < 0)
                bird.velocity = 0;
            bird.velocity += 0.32;
            bird.y += bird.velocity;

            if (bird.y + bird.height >= background.height - ground.height)
                bird.y = background.height - ground.height - bird.height;
            else if (
                (
                    bird.x + bird.width > pipes.top.x[0] + 2
                    && bird.x < pipes.top.x[0] + 2 + pipes.top.width
                )
                && bird.y + bird.height >= pipes.bottom.y[0] + 2
            )
                bird.y = pipes.bottom.y[0] + 2 - bird.height;
        } else
            game.state = 3;
    }
};

document.addEventListener("keydown", function(e) {
    if (e.keyCode === 32) {        
        if (game.state === 0 || game.state === 3) {
            game.restart();
            updateScore(game.score);
            game.state = 1;
        } else if (game.state === 1) {
            bird.velocity = -5;
        }
    }
});
