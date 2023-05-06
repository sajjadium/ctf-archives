import "./App.css";
import { Grid } from "@material-ui/core";
import { Card } from "@material-ui/core";
import SignIn from "./components/Signin";
import SignUp from "./components/Signup";
import AppBar from "@material-ui/core/AppBar";
import Typography from "@material-ui/core/Typography";
import Toolbar from "@material-ui/core/Toolbar";
import { useState } from "react";
import { useEffect } from "react";
import { Route } from "react-router-dom";
import ReactCardFlip from "react-card-flip";
import { useHistory } from "react-router-dom";
import HomePage from "./components/HomePage";
import validator from "validator";
import axios from "axios";
import Cookies from "js-cookie";
import { useLocation } from "react-router-dom";

function App() {
  const history = useHistory();
  const location = useLocation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [emailWarn, setEmailWarn] = useState(false);
  const [passwordWarn, setPasswordWarn] = useState(false);
  const [name, setName] = useState("");
  const [region, setRegion] = useState("eu");
  const [flipped, setFlipped] = useState(false);

  useEffect(() => {
    if (Cookies.get("token") && location.pathname === "/") {
      window.location.href = Cookies.get("regionURL");
    }
  }, [history]);
  const changeEmail = (email) => {
    setEmail(email);
    if (validator.isEmail(email)) {
      setEmailWarn(false);
    } else {
      setEmailWarn(true);
    }
  };
  const changePassword = (password) => {
    setPassword(password);
    if (
      validator.isStrongPassword(password, {
        minLength: 8,
        minLowercase: 0,
        minUppercase: 0,
        minNumbers: 0,
        minSymbols: 1,
      })
    ) {
      setPasswordWarn(false);
    } else {
      setPasswordWarn(true);
    }
  };
  const login = () => {
    if (
      validator.isEmail(email) &&
      validator.isStrongPassword(password, {
        minLength: 8,
        minLowercase: 0,
        minUppercase: 0,
        minNumbers: 0,
        minSymbols: 1,
      })
    ) {
      var data = JSON.stringify({
        email: email,
        password: password,
      });

      var config = {
        method: "post",
        url: "/api/login",
        headers: {
          "Content-Type": "application/json",
        },
        data: data,
      };

      axios(config)
        .then(function (response) {
          Cookies.set("token", response.data.token, {
            expires: 365,
            secure: true,
          });
          history.push("/home");
        })
        .catch(function (error) {
        });
    }
  };

  const register = () => {
    if (
      validator.isEmail(email) &&
      validator.isStrongPassword(password, {
        minLength: 8,
        minLowercase: 0,
        minUppercase: 0,
        minNumbers: 0,
        minSymbols: 1,
      })
    ) {
      var data = JSON.stringify({
        email: email,
        password: password,
        name: name,
        region: region,
      });

      var config = {
        method: "post",
        url: "/api/users",
        headers: {
          "Content-Type": "application/json",
        },
        data: data,
      };

      axios(config)
        .then(function (response) {

          var data = JSON.stringify({
            region: "https://" + region + ".r41k0u.me/home",
          });

          var config = {
            method: "post",
            url: "/api/region",
            headers: {
              "Content-Type": "application/json",
            },
            data: data,
            withCredentials: true,
          };

          axios(config)
            .then(function (response) {
              window.location.reload();
            })
            .catch(function (error) {
              console.log(error);
            });
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  };

  return (
    <div className="App">
      <Route
        path="/"
        exact
        render={(props) => (
          <>
            <div className="login">
              <Grid
                container
                direction="column"
                justify="center"
                alignItems="center"
                style={{ minHeight: "100vh", background: "#fafafa" }}
              >
                <Grid container item xs={3}>
                  <AppBar style={{ alignItems: "flex-start" }}>
                    <Toolbar>
                      <Grid container justify="flex-start">
                        <Typography variant="h4" color="inherit" noWrap>
                          Fl4sh
                        </Typography>
                      </Grid>
                    </Toolbar>
                  </AppBar>
                </Grid>
                <Grid container item xs={3}>
                  <ReactCardFlip isFlipped={flipped} flipDirection="vertical">
                    <Card elevation={3}>
                      <SignIn
                        email={email}
                        changeEmail={changeEmail}
                        password={password}
                        changePassword={changePassword}
                        onLogin={login}
                        setFlip={setFlipped}
                        emailWarn={emailWarn}
                        passwordWarn={passwordWarn}
                      ></SignIn>
                    </Card>
                    <Card elevation={3}>
                      <SignUp
                        email={email}
                        changeEmail={changeEmail}
                        password={password}
                        changePassword={changePassword}
                        name={name}
                        setName={setName}
                        setFlip={setFlipped}
                        onRegister={register}
                        emailWarn={emailWarn}
                        passwordWarn={passwordWarn}
                        region={region}
                        setRegion={setRegion}
                      ></SignUp>
                    </Card>
                  </ReactCardFlip>
                </Grid>
              </Grid>
            </div>
          </>
        )}
      />
      <Route path="/home/:teamSecret?">
        <HomePage />
      </Route>
    </div>
  );
}

export default App;
