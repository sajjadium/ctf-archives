var current = null;
document.querySelector('#user').addEventListener('focus', function(e) {
  if (current) current.pause();
  current = anime({
    targets: 'path',
    strokeDashoffset: {
      value: 0,
      duration: 700,
      easing: 'easeOutQuart'
    },
    strokeDasharray: {
      value: '240 1386',
      duration: 700,
      easing: 'easeOutQuart'
    }
  });
});
document.querySelector('#password').addEventListener('focus', function(e) {
  if (current) current.pause();
  current = anime({
    targets: 'path',
    strokeDashoffset: {
      value: -336,
      duration: 700,
      easing: 'easeOutQuart'
    },
    strokeDasharray: {
      value: '240 1386',
      duration: 700,
      easing: 'easeOutQuart'
    }
  });
});
document.querySelector('#submit').addEventListener('focus', function(e) {
  if (current) current.pause();
  current = anime({
    targets: 'path',
    strokeDashoffset: {
      value: -730,
      duration: 700,
      easing: 'easeOutQuart'
    },
    strokeDasharray: {
      value: '530 1386',
      duration: 700,
      easing: 'easeOutQuart'
    }
  });
});


let login = () => {
    var user = document.getElementById("user");
    var password = document.getElementById("password");

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user: user.value,
            password: password.value
        })
    }).then((response) => {
        console.log(response);
        if (response.ok) {
            response.json().then((data) => {
                if (data.status === "ok") {
                    cookie = response.headers.get("Set-Cookie");
                    document.cookie = cookie;
                    window.location.href = "/dashboard";
                } else {
                    alert("Invalid username or password");
                }
            });
        } else {
            alert("Invalid username or password");
        }
    });
}
