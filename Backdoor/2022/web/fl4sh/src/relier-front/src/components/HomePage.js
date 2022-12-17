import { Avatar, Button, CardActionArea, Fab } from "@material-ui/core";
import axios from "axios";
import Cookies, { set } from "js-cookie";
import { useEffect, useState } from "react";
import { Link, useHistory, useParams } from "react-router-dom";
import React from "react";
import AppBar from "@material-ui/core/AppBar";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";

import CssBaseline from "@material-ui/core/CssBaseline";
import Grid from "@material-ui/core/Grid";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

import { deepOrange } from "@material-ui/core/colors";
import VideoCallIcon from "@material-ui/icons/VideoCall";
import TextField from "@material-ui/core/TextField";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";

const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(2),
  },
  heroContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(1, 0, 5),
  },
  heroButtons: {
    marginTop: theme.spacing(4),
  },
  cardGrid: {
    paddingTop: theme.spacing(8),
    paddingBottom: theme.spacing(8),
  },
  card: {
    height: "100%",
    display: "flex",
    flexDirection: "column",
  },
  cardMedia: {
    paddingTop: "56.25%", // 16:9
  },
  cardContent: {
    flexGrow: 1,
  },
  orange: {
    color: theme.palette.getContrastText(deepOrange[500]),
    backgroundColor: deepOrange[500],
  },
  extendedIcon: {
    marginRight: theme.spacing(1),
  },
  fab: {
    position: "fixed",
    bottom: theme.spacing(8),
    right: theme.spacing(8),
  },
}));

export default function HomePage() {
  const { teamSecret } = useParams();
  const [createTeamOpen, setCreateTeamOpen] = useState(false);
  const [reportOpen, setReportOpen] = useState(false);
  const [malURL, setMalURL] = useState("");
  const [images, setImages] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const classes = useStyles();
  const history = useHistory();

  const onFileChange = (event) => {
    // Update the state
    setSelectedFile({ selectedFile: event.target.files[0] });
  };

  const onFileUpload = () => {
    const formData = new FormData();

    formData.append("image", selectedFile.selectedFile, selectedFile.selectedFile.name);

    console.log(formData);

    var config = {
      method: "post",
      url: `/api/secure/images/`,
      headers: {
        Authorization: `Bearer ${Cookies.get("token")}`,
        "Content-Type": "multipart/form-data",
      },
      data: formData,
    };

    axios(config)
      .then(function (response) {
        console.log(JSON.stringify(response.data));
        loadImages();
        handleCreateClose();
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  const onReport = () => {
    var data = { url: malURL };

    var config = {
      method: "post",
      url: `/api/secure/report/`,
      headers: {
        Authorization: `Bearer ${Cookies.get("token")}`,
      },
      data: data,
    };

    axios(config)
      .then(function (response) {
        console.log(JSON.stringify(response.data));
        handleReportClose();
      })
      .catch(function (error) {
        console.log(error);
      });
  };


  useEffect(() => {
    if (!Cookies.get("token")) {
      history.push("/");
    }
  }, [history]);

  useEffect(() => {
    loadImages();
  }, []);

  function loadImages() {
    console.log("bla");
    var config = {
      method: "get",
      url: "/api/secure/images/",
      headers: {
        Authorization: `Bearer ${Cookies.get("token")}`,
      },
    };

    axios(config)
      .then(function (response) {
        console.log(JSON.stringify(response.data));
        setImages(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  const handleCreateOpen = () => {
    setCreateTeamOpen(true);
  };

  const handleCreateClose = () => {
    setCreateTeamOpen(false);
  };
  const handleReportOpen = () => {
    setReportOpen(true);
  };

  const handleReportClose = () => {
    setReportOpen(false);
  };


  return (
    <>
      <Fab variant="extended" className={classes.fab} color="primary" onClick={handleReportOpen}>
        <VideoCallIcon className={classes.extendedIcon} />
        Report Image to Admin
      </Fab>
      <div>
        <Dialog
          open={createTeamOpen}
          onClose={handleCreateClose}
          aria-labelledby="form-dialog-title"
          maxWidth="xs"
          fullWidth={true}
        >
          <DialogTitle id="form-dialog-title">Upload New Image</DialogTitle>
          <DialogContent>
            {/* upload image here */}
            <input type="file" onChange={onFileChange} />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCreateClose} color="primary">
              Cancel
            </Button>
            <Button onClick={onFileUpload} color="primary">
              Upload
            </Button>
          </DialogActions>
        </Dialog>
      </div>
      <div>
        <Dialog
          open={reportOpen}
          onClose={handleReportClose}
          aria-labelledby="form-dialog-title"
          maxWidth="xs"
          fullWidth={true}
        >
          <DialogTitle id="form-dialog-title">Report Malicious Image</DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              id="url"
              label="Malicious Image URL"
              fullWidth
              value={malURL}
              onChange={(e) => setMalURL(e.target.value)}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleReportClose} color="primary">
              Cancel
            </Button>
            <Button onClick={onReport} color="primary">
              Report
            </Button>
          </DialogActions>
        </Dialog>
      </div>
      <CssBaseline />
      <AppBar position="relative">
        <Toolbar>
          <Grid container justify="flex-start">
            <Typography variant="h4" color="inherit" noWrap>
              Fl4sh
            </Typography>
          </Grid>
          <Grid container justify="flex-end">
            <Button
              color="inherit"
              variant="outlined"
              onClick={() => {
                Cookies.remove("token");
                history.push("/");
              }}
            >
              Logout
            </Button>
          </Grid>
        </Toolbar>
      </AppBar>
      <main>
        <Container className={classes.cardGrid} maxWidth="md">
          {/* End hero unit */}
          <Grid container spacing={4}>
            <Grid item xs={12} sm={6} md={4}>
              <Card
                className={classes.card}
                style={{
                  alignItems: "center",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "center",
                }}
              >
                <CardContent
                  style={{
                    alignItems: "center",
                    display: "flex",
                    // flexDirection: "column",
                    justifyContent: "center",
                  }}
                >
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleCreateOpen}
                  >
                    Upload Image
                  </Button>
                </CardContent>
              </Card>
            </Grid>
            {images.map((image) => (
              <Grid item xs={12} sm={6} md={4}>
                <Card className={classes.card} hoverable>
                  <div style={{ cursor: "pointer" }}>
                    <Link
                      to={`/cdn/${image}`}
                      style={{ textDecoration: "none" }}
                      target="_blank"
                    >
                      <CardContent
                        style={{
                          alignItems: "center",
                          display: "flex",
                          // flexDirection: "column",
                          paddingBottom: 0,
                          justifyContent: "center",
                        }}
                      >
                        <Avatar className={classes.orange} variant="square">
                          {image.substring(0, 1)}
                        </Avatar>
                      </CardContent>
                      <CardContent
                        className={classes.cardContent}
                        style={{ paddingBottom: 0 }}
                      >
                        <Typography gutterBottom variant="h5" component="h2">
                          {image}
                        </Typography>
                      </CardContent>
                    </Link>
                  </div>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </main>
    </>
  );
}
