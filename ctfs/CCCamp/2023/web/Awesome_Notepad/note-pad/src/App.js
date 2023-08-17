import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Container from '@material-ui/core/Container';
import Box from '@material-ui/core/Box';
import Main from './components/Main';
import Header from './components/Header';
import ErrorBoundary from './ErrorBoundary';
import NewNote from './components/NewNote';
import NewTicket from './components/NewTicket';

export default function App() {
    return (
        <Router>
            <Switch>
                <Route path="/new">
                    <Content>
                        <NewNote note={{ body: '', title: '' }} />
                    </Content>
                </Route>

                <Route path="/newTicket">
                    <Content>
                        <NewTicket ticket={{ issue: ''}} />
                    </Content>
                </Route>

                <Route path="/note/:noteId">
                    <Content>
                        <Main />
                    </Content>
                </Route>

                <Route path="/">
                    <Content>
                        <Main />
                    </Content>
                </Route>
            </Switch>
        </Router>
    );
}

const Content = props => (
    <ErrorBoundary>
        <Container maxWidth="lg">
            <Header />
            <Box my={4}>{props.children}</Box>
        </Container>
    </ErrorBoundary>
);
