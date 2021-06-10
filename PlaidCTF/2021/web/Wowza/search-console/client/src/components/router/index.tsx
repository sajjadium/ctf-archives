import * as React from "react";
import { Switch, Router, Route, Redirect } from "react-router-dom";

import { History } from "../../history";
import { UserContext } from "../../providers/user-provider";
import { Login, Register } from "../login";
import { SiteList } from "../site-list";

export interface Props {

}

const Loading = () => <h1>Loading...</h1>;

export const ConsoleRouter = (props: Props) => {
    const { user } = React.useContext(UserContext);

    return (
        <Router history={History}>
            <Switch>
                <Route path="/login" component={Login}/>
                <Route path="/register" component={Register}/>
                {
                    user.value !== undefined ? <Route path="/" exact component={SiteList}/> :
                    user.loading ? <Route path="/" component={Loading}/> :
                    <Redirect to="/login"/>
                }
            </Switch>
        </Router>
    )
}