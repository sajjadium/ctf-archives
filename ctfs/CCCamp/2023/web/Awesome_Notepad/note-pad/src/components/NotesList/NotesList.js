import React from 'react';
import Paper from '@material-ui/core/Paper';
import { Link as RouterLink } from 'react-router-dom';
import Link from '@material-ui/core/Link';
import useStyles from './style';

const WrappedLink = React.forwardRef((props, ref) => (
    <RouterLink innerRef={ref} {...props} />
));

const NotesListItem = ({ id, title, classes }) => (
    <li data-testid="noteItem" className={classes.listItem}>
        <Link component={WrappedLink} to={`/note/${id}`}>
            <Paper className={classes.paper}>{title}</Paper>
        </Link>
    </li>
);

export default function NotesList({ notes }) {
    const classes = useStyles();

    return (
        <ul className={classes.list}>
            {notes.map(note => (
                <NotesListItem
                    key={note.id}
                    classes={classes}
                    id={note.id}
                    title={note.title}
                />
            ))}
        </ul>
    );
}
