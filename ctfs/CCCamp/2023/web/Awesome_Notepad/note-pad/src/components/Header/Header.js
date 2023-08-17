import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { Link as RouterLink } from 'react-router-dom';
import Link from '@material-ui/core/Link';
import useStyles from './style';
import AddCircleOutlineIcon from '@material-ui/icons/AddCircleOutline';
import BugReportIcon from '@material-ui/icons/BugReport';
import IconButton from '@material-ui/core/IconButton';

const WrappedLink = React.forwardRef((props, ref) => (
    <RouterLink innerRef={ref} {...props} />
));

export default function Header() {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>
                    <Typography className={classes.title} variant="h6" noWrap>
                        <Link
                            component={WrappedLink}
                            className={classes.link}
                            to={`/`}
                        >
                            Taking Notes
                        </Link>
                    </Typography>
                    <Link
                        component={WrappedLink}
                        className={classes.link}
                        to={`/new`}
                    >
                        <IconButton
                            aria-label="show 17 new notifications"
                            color="inherit"
                        >
                            <AddCircleOutlineIcon />
                        </IconButton>
                    </Link>
                    <Link
                        component={WrappedLink}
                        className={classes.link}
                        to={`/newTicket`}
                    >
                        <IconButton
                            aria-label="show 17 new notifications"
                            color="inherit"
                        >
                            <BugReportIcon />
                        </IconButton>
                    </Link>
                </Toolbar>
            </AppBar>
        </div>
    );
}
