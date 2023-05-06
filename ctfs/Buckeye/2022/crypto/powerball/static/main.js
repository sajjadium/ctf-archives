const socket = io() // eslint-disable-line no-undef
let seenFlag = false

function seedToBalls (n) {
  const balls = []
  for (let i = 0; i < 10; i++) {
    balls.push(Number(n % 100n))
    n = n / 100n
  }
  return balls
}

function handleUpdate (update) {
  console.log(update)

  if (update.flag && !seenFlag) {
    alert(update.flag)
    seenFlag = true
  }

  const balls = seedToBalls(BigInt(update.last_winning_seed))
  for (let i = 0; i < 10; i++) {
    document.getElementById(`ball${i}`).innerText = balls[i]
  }
}

function initSocket () {
  socket.on('update', handleUpdate)
  socket.emit('updateRequest')

  setInterval(() => {
    console.log(Date.now() / 1000)
    socket.emit('updateRequest')
  }, 5000)
}

function sendBallsIfAvailable () {
  const balls = []
  for (let i = 0; i < 10; i++) {
    const a = parseInt(document.getElementById(`input-ball${i}`).value)
    if (isNaN(a) || a < 0 || a >= 100) return
    balls.push(a)
  }
  console.log(`Submitting balls ${balls}`)
  socket.emit('submitBalls', balls)
}

function initInput () {
  for (let i = 0; i < 10; i++) {
    document.getElementById(`input-ball${i}`).onkeypress = (event) => {
      const n = parseInt(event.key)
      if (isNaN(n)) return false
      setTimeout(sendBallsIfAvailable, 100)
    }
    document.getElementById(`input-ball${i}`).onpaste = (event) => {
      const n = event.clipboardData.getData('Text')
      if (isNaN(n)) return false
      setTimeout(sendBallsIfAvailable, 100)
    }
  }
}

initSocket()
initInput()
