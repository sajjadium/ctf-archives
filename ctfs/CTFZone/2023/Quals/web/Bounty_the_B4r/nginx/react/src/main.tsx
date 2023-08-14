import React from "react"
import ReactDOM from "react-dom/client"
import { Route, Switch } from "wouter"
import Auth from "./Auth"
import App from "./App"
import { Toaster } from "@/components/ui/toaster"
import { UserContextProvider } from "./useUser"
import "./index.css"

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <UserContextProvider>
      <Switch>
        <Route path="/login">
          <Auth type="login" />
        </Route>
        <Route path="/register">
          <Auth type="registration" />
        </Route>
        <Route path="/report/:id">
          <App />
        </Route>
        <Route path="/:rest*">
          <App />
        </Route>
      </Switch>
      <Toaster />
    </UserContextProvider>
  </React.StrictMode>,
)
