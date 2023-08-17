import React from 'react';
import { render } from 'react-dom';
import ApolloClient from 'apollo-boost';
import { ApolloProvider } from 'react-apollo';
import CssBaseline from '@material-ui/core/CssBaseline';
import { ThemeProvider } from '@material-ui/core/styles';
import App from './App';
import theme from './theme';

// Pass your GraphQL endpoint to uri
const client = new ApolloClient({
    uri: `${window.config.REACT_APP_API_ROOT}/graphql`
});

const ApolloApp = () => (
    <ApolloProvider client={client}>
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <App />
        </ThemeProvider>
    </ApolloProvider>
);

render(ApolloApp(App), document.getElementById('root'));
