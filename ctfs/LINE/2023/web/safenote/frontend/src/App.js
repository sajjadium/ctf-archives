import "bootstrap/dist/css/bootstrap.min.css"
import "./App.css"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import { useState } from "react"
import Register from "./Component/Register"
import Navi from "./Component/Navi"
import Home from "./Component/Home"
import Login from "./Component/Login"
import Note from "./Component/Note"
import Create from "./Component/Create"

const USER_API_INFO = "/api/user/info";

function App() {
  const [auth, setAuth] = useState(localStorage.token? true : false);

  const authRequired = () => {
      if (localStorage.token) {
          fetch(USER_API_INFO, {
              method: "GET",
              headers: {
                  "Authorization": `Bearer ${localStorage.token}`,
              },
          }).then(res => {
              if (res.data && res.data.result) {
                  setAuth(true);
              }
              if (res.status !== 200){
                  localStorage.removeItem("token");
              }
          })
      }else{
              setAuth(false);
              localStorage.removeItem("token");
      }
  }

  return (
    <div className="App">
        <Navi auth={auth} authRequired={authRequired}/>
        <BrowserRouter>
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/note" element={<Note auth={auth} authRequired={authRequired}/>}   />
            <Route path="/create" element={<Create auth={auth} authRequired={authRequired}/>} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
        </Routes>
        </BrowserRouter>
    </div>
  )
}

export default App