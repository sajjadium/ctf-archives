style = `.animation0 {
    font-size: 42px;
    font-family: Arial Black, Gadget, sans-serif;
    background-image: -webkit-linear-gradient(left, #f00, #ff2b00, #f50, #ff8000, #fa0, #ffd500, #ff0, #d4ff00, #af0, #80ff00, #5f0, #2bff00, #0f0, #00ff2a, #0f5, #00ff80, #0fa, #00ffd5, #0ff, #00d5ff, #0af, #0080ff, #05f, #002aff, #00f, #2b00ff, #50f, #8000ff, #a0f, #d400ff, #f0f, #ff00d4, #f0a, #ff0080, #f05, #ff002b, #f00);
    -webkit-animation: animatedBackground_a 5s linear infinite alternate;
    -webkit-background-clip: text;
    -webkit-text-fill-color: #0000;
    background-clip: text;
}

@keyframes animatedBackground_a {
    0% { background-position: 0 0 }
    100% { background-position: -500px 0 }
}

.animation1 {
    background-color: pink;
    font-size: 42px;
    font-family: Arial Black, Gadget, sans-serif;
    -webkit-animation: animatedBackground_b 5s linear infinite alternate;
}

@keyframes animatedBackground_b{
    0% {color: #ff8b00}
    10% {color: #e8ff00}
    20% {color: #5dff00}
    30% {color: #00ff2e}
    40% {color: #00ffb9}
    50% {color: #00b9ff}
    60% {color: #002eff}
    70% {color: #5d00ff}
    80% {color: #e800ff}
    90% {color: #ff008b}
    100% {color: #ff0000}
}
.animation2 {
    background-color: black;
    background-image: linear-gradient(0deg, #f00 25%, #ffb300 60%);
    color: #0000;
    -webkit-background-clip: text;
    background-clip: text;
    font-size: 50px;
    font-weight: bold;
    display: inline-block;
}
.animation3 {
    background-color: black;
    color: #F00;
    -webkit-text-fill-color: transparent;
    font-size: 42px;
    font-family: Arial Black, Gadget, sans-serif;
    -webkit-text-stroke-width: 2px;
    -webkit-text-stroke-color: #FF0000;
    -webkit-animation: animatedBackground_c 2s infinite alternate;
}

@keyframes animatedBackground_c {
    0% {-webkit-text-stroke-color: #ff8b00}
    10% {-webkit-text-stroke-color: #e8ff00}
    20% {-webkit-text-stroke-color: #5dff00}
    30% {-webkit-text-stroke-color: #00ff2e}
    40% {-webkit-text-stroke-color: #00ffb9}
    50% {-webkit-text-stroke-color: #00b9ff}
    60% {-webkit-text-stroke-color: #002eff}
    70% {-webkit-text-stroke-color: #5d00ff}
    80% {-webkit-text-stroke-color: #e800ff}
    90% {-webkit-text-stroke-color: #ff008b}
    100% {-webkit-text-stroke-color: #ff0000}
}
:root {
  --shadow-color: #FF9E9E;
  --shadow-color-light: white;
}

* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}


p {
  font-size: 45px;
  text-transform: uppercase;
  font-family: "Archivo Black", "Archivo", sans-serif;
  font-weight: normal;
  display: block;
  height: auto;
  text-align: center;
}

.animation4 {
  background-color: black;
  color: white;
  animation: neon 2s infinite;
}

@keyframes neon {
  0% {
    text-shadow: -1px -1px 1px var(--shadow-color-light), -1px 1px 1px var(--shadow-color-light), 1px -1px 1px var(--shadow-color-light), 1px 1px 1px var(--shadow-color-light),
    0 0 3px var(--shadow-color-light), 0 0 10px var(--shadow-color-light), 0 0 20px var(--shadow-color-light),
    0 0 30px var(--shadow-color), 0 0 40px var(--shadow-color), 0 0 50px var(--shadow-color), 0 0 70px var(--shadow-color), 0 0 100px var(--shadow-color), 0 0 200px var(--shadow-color);
  }
  50% {
    text-shadow: -1px -1px 1px var(--shadow-color-light), -1px 1px 1px var(--shadow-color-light), 1px -1px 1px var(--shadow-color-light), 1px 1px 1px var(--shadow-color-light),
    0 0 5px var(--shadow-color-light), 0 0 15px var(--shadow-color-light), 0 0 25px var(--shadow-color-light),
    0 0 40px var(--shadow-color), 0 0 50px var(--shadow-color), 0 0 60px var(--shadow-color), 0 0 80px var(--shadow-color), 0 0 110px var(--shadow-color), 0 0 210px var(--shadow-color);
  }
  100% {
    text-shadow: -1px -1px 1px var(--shadow-color-light), -1px 1px 1px var(--shadow-color-light), 1px -1px 1px var(--shadow-color-light), 1px 1px 1px var(--shadow-color-light),
    0 0 3px var(--shadow-color-light), 0 0 10px var(--shadow-color-light), 0 0 20px var(--shadow-color-light),
    0 0 30px var(--shadow-color), 0 0 40px var(--shadow-color), 0 0 50px var(--shadow-color), 0 0 70px var(--shadow-color), 0 0 100px var(--shadow-color), 0 0 200px var(--shadow-color);
  }
}
a {
    text-decoration: none;
    color: #9ca0b1;
}

$avatar-size: 32px;
$body-background: #353535;

body {
    height: 100vh;
    margin: 0;
    background-color: $body-background;
    font-family: "ubuntu", Arial, sans-serif;
    overflow-x: hidden;
    display: grid;
    place-items: center;
}

a {
    text-decoration: none;
    color: #9ca0b1;
}


.animation5 {

  background: #f08080;
  color: powderblue;
  font-size: 3em;
  font-family: sans-serif;
  letter-spacing: 0.1em;
  transition: 0.3s;
  text-shadow: 1px 1px 0 grey, 1px 2px 0 grey, 1px 3px 0 grey, 1px 4px 0 grey,
    1px 5px 0 grey, 1px 6px 0 grey, 1px 7px 0 grey, 1px 8px 0 grey,
    5px 13px 15px black;
}



`