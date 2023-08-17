import React, { useState } from 'react';
import { useMutation } from '@apollo/react-hooks';
import { Redirect } from 'react-router-dom';
import Paper from '@material-ui/core/Paper';
import { gql } from 'apollo-boost';
import InputBase from '@material-ui/core/InputBase';
import FormControl from '@material-ui/core/FormControl';
import Button from '@material-ui/core/Button';
import SendIcon from '@material-ui/icons/Send';
import useStyles from './style';

const SAVE_TICKET = gql`
    mutation addTicket($issue: String) {
        addTicket(issue: $issue) {
            issue
        }
    }
`;

export default function NewTicket({ initial }) {
    const classes = useStyles();
    const [ticket, setTicket] = useState({ initial });
    const [toHome, setToHome] = useState(false);
    const [saveTicket] = useMutation(SAVE_TICKET);

    const onSend = () => {
        if (!ticket.issue) return;
        saveTicket({ variables: ticket });
        setToHome(true);
    };

    return (
        <div>
            <h1>Send a bug report to the admin:</h1>
            {toHome ? <Redirect to="/"></Redirect> : null}
            <Paper className={classes.paper}>
                <FormControl fullWidth className={classes.margin}>
                    <InputBase
                        autoFocus
                        multiline
                        aria-label="minimum height"
                        rows={15}
                        onChange={e => {
                            setTicket({
                                ...ticket,
                                issue: e.target.value
                            });
                        }}
                        value={ticket.issue}
                    />
                </FormControl>
                <div>
                    <Button
                        data-testid="send"
                        variant="contained"
                        color="primary"
                        size="large"
                        className={classes.button}
                        onClick={onSend}
                        value={ticket.issue}
                        startIcon={<SendIcon />}
                    >
                        Send
                    </Button>
                </div>
            </Paper>
        </div>
    );
}
