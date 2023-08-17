import React, { useState } from 'react';
import { useMutation } from '@apollo/react-hooks';
import { Redirect } from 'react-router-dom';
import Paper from '@material-ui/core/Paper';
import { gql } from 'apollo-boost';
import InputBase from '@material-ui/core/InputBase';
import FormControl from '@material-ui/core/FormControl';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';
import TextField from '@material-ui/core/TextField';
import useStyles from './style';

const SAVE_NOTE = gql`
    mutation addNote($title: String, $body: String) {
        addNote(title: $title, body: $body) {
            title
            body
        }
    }
`;

export default function NewNote({ initial }) {
    const classes = useStyles();
    const [note, setNote] = useState({ initial });
    const [toHome, setToHome] = useState(false);
    const [saveNote] = useMutation(SAVE_NOTE);

    const onSave = () => {
        if (!note.title) return;
        saveNote({ variables: note });
        setToHome(true);
    };

    return (
        <div>
            {toHome ? <Redirect to="/"></Redirect> : null}
            <Paper className={classes.paper}>
                <FormControl fullWidth className={classes.margin}>
                    <InputBase
                        autoFocus
                        multiline
                        aria-label="minimum height"
                        rows={15}
                        onChange={e => {
                            setNote({
                                ...note,
                                body: e.target.value
                            });
                        }}
                        value={note.body}
                    />
                </FormControl>

                <TextField
                    required
                    className={classes.textField}
                    label="Note Titel"
                    margin="normal"
                    variant="outlined"
                    onChange={e => {
                        setNote({
                            ...note,
                            title: e.target.value
                        });
                    }}
                />
                <div>
                    <Button
                        data-testid="save"
                        variant="contained"
                        color="primary"
                        size="large"
                        className={classes.button}
                        onClick={onSave}
                        value={note.title}
                        startIcon={<SaveIcon />}
                    >
                        Save
                    </Button>
                </div>
            </Paper>
        </div>
    );
}
