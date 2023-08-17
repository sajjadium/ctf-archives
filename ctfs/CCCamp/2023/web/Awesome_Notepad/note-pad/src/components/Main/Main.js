import React from 'react';
import Grid from '@material-ui/core/Grid';
import { gql } from 'apollo-boost';
import { Query } from 'react-apollo';
import { useParams } from 'react-router-dom';
import NotesList from '../NotesList';
import NoteDisplay from '../NoteDisplay';
import useStyles from './style';

const GET_NOTES = gql`
    query {
        notes {
            id
            title
            body
        }
    }
`;

export default function Main() {
    const classes = useStyles();
    const { noteId } = useParams();

    return (
        <Query query={GET_NOTES} fetchPolicy={'network-only'}>
            {({ loading, error, data = [] }) => {
                if (loading) return <div>Loading...</div>;
                if (error) {
                    return <div>Something is horribly wrong</div>;
                }

                return (
                    <div className={classes.root}>
                        <Grid container spacing={3}>
                            <Grid item xs={12} sm={4} ms={4} lg={4} xl={4}>
                                <NotesList notes={data.notes}></NotesList>
                            </Grid>
                            <Grid item xs={12} sm={8} ms={8} lg={8} xl={8}>
                                <NoteDisplay
                                    note={
                                        data.notes.filter(
                                            note => note.id === noteId
                                        )[0]
                                    }
                                />
                            </Grid>
                        </Grid>
                    </div>
                );
            }}
        </Query>
    );
}
