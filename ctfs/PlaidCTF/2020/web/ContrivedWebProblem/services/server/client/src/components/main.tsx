import * as React from "react";
import { Helmet } from "react-helmet";
import {
    BrowserRouter,
    Switch,
    Route,
} from "react-router-dom";

import Home from "./home";

import { SiteContext, SiteKind } from "../contexts/site";
import { UserProvider } from "../contexts/user";

import { unreachable } from "../utils/utils";

import Header from "./header";
import Login from "./login";
import Profile from "./profile";
import Nav from "./nav";

import "./main.scss";

const frameworks = [
    "https://unpkg.com/purecss@1.0.1/build/pure-min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css",
    "https://getbootstrap.com/1.1.1/assets/css/bootstrap-1.1.1.min.css",
];

export type Props = {
    title?: string;
}

export default (props: Props) => {
    let [framework] = React.useState(Math.floor(Math.random() * 3));
    let [siteKind] = React.useState((Math.floor(Math.random() * 3) + 1) as SiteKind);


    let cssFramework =
        framework === 0 ? "css-pure" :
        framework === 1 ? "css-materialize" :
        "css-bootstrap";

    let siteClass =
        siteKind === SiteKind.NOTE_APP ? "kind-note-app" :
        siteKind === SiteKind.FORUM ? "kind-forum" :
        siteKind === SiteKind.BUG_PORTAL ? "kind-bug-portal" :
        unreachable(siteKind);

    return (
        <main className={`main-site ${cssFramework} ${siteClass}`}>
            <SiteContext.Provider value={{ kind: siteKind }}>
            <UserProvider>
                <BrowserRouter>
                <Helmet>
                    <link rel="stylesheet" href={frameworks[framework]} />
                </Helmet>
                <Header/>
                <Nav/>
                    <div className="site-content">
                        <Switch>
                            <Route path="/" exact={true}>
                            <Home/>
                            </Route>
                            <Route path="/login" exact={true}>
                                <Login />
                            </Route>
                            <Route path="/register" exact={true}>
                                <Login register/>
                            </Route>
                            <Route path="/profile" exact={true}>
                                <Profile/>
                            </Route>
                        </Switch>
                    </div>
                </BrowserRouter>
            </UserProvider>
            </SiteContext.Provider>
        </main>
    );
}