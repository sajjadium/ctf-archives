import React, { useState, useEffect } from 'react';
import { useMutation } from '@apollo/react-hooks';
import { Redirect } from 'react-router-dom';
import Paper from '@material-ui/core/Paper';
import { gql } from 'apollo-boost';
import InputBase from '@material-ui/core/InputBase';
import FormControl from '@material-ui/core/FormControl';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';
import DeleteIcon from '@material-ui/icons/Delete';
import Snackbar from '@material-ui/core/Snackbar';
import useStyles from './style';

const SAVE_NOTE = gql`
    mutation saveNote($id: String, $title: String, $body: String) {
        saveNote(id: $id, title: $title, body: $body) {
            id
            title
            body
        }
    }
`;

const DELETE_NOTE = gql`
    mutation deleteNote($id: String) {
        deleteNote(id: $id) {
            status
            message
        }
    }
`;

export default function NotesDisplay({ note }) {
    const classes = useStyles();
    const [currentNote, setCurrentNote] = useState(note);
    const [toHome, setToHome] = useState(false);
    const [open, setOpen] = useState(false);
    const [del, setDelete] = useState(false);
    const [saveNote] = useMutation(SAVE_NOTE);
    const [deleteNote] = useMutation(DELETE_NOTE);

    useEffect(() => {
        setCurrentNote(note);
        setToHome(false);
    }, [note]);

    const onSave = () => {
        saveNote({ variables: currentNote });
        setOpen(true);
        setTimeout(() => setOpen(false), 1500);
    };

    const onDelete = () => {
        deleteNote({ variables: { id: currentNote.id } });
        setDelete(true);
        //temporary fix until I can figure out why state is not updated in NoteList
        setTimeout(() => setDelete(false), 500);
        setTimeout(() => window.location.reload(1), 700);
    };
    if (!currentNote) return <div></div>;
    return (
        <div>
            {toHome ? <Redirect to="/"></Redirect> : null}
            <Paper className={classes.paper}>
                <FormControl fullWidth className={classes.margin}>
                    <InputBase
                        multiline
                        aria-label="minimum height"
                        rows={15}
                        onChange={e =>
                            setCurrentNote({ ...note, body: e.target.value })
                        }
                        value={currentNote.body}
                    />
                </FormControl>
                <Button
                    variant="contained"
                    color="primary"
                    size="large"
                    className={classes.button}
                    onClick={onSave}
                    startIcon={<SaveIcon />}
                >
                    Save
                </Button>
                <Button
                    variant="contained"
                    color="secondary"
                    size="large"
                    className={classes.button}
                    onClick={onDelete}
                    startIcon={<DeleteIcon />}
                >
                    Delete
                </Button>
            </Paper>

            <Snackbar
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                key={`bottom,right`}
                open={open}
                message={<span>{note ? note.title : ''} has been saved.</span>}
            />
            <Snackbar
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                key={`bottom,right`}
                open={del}
                message={<span>{note ? note.title : ''} has been deleted.</span>}
            />
        </div>
    );
}
