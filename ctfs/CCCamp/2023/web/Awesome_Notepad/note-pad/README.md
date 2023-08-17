# Taking Notes

## Overview

This is a note taking application. Implemented features are

-   Create a note
-   Edit and save notes
-   Delete notes

All notes are being persited in a database.

### Architecture

The application consist of a **React** application and a [**GraphQL backend API**](https://github.com/FilipStenbeck/note-app-api).
The API is needed for the application to run, so make sure the API is up before starting the frontend application.
This repo includes a node express webserver that can be used for servering the app once it is built. See below for instructions on how to start the application.

### Dependencies (major)

List of major libraries and tools:

-   [React](https://github.com/facebook/react) (and [create-react-app](https://github.com/facebook/create-react-app))
-   [React Router](https://github.com/ReactTraining/react-router)
-   [Apollo GraphQL](https://github.com/apollographql)
-   [Material-UI](https://github.com/mui-org/material-ui)
-   [Express](https://github.com/expressjs/express)

# How to use

## Quickstart
The fastest way to get the app and API up and running is using Docker. Both images are pushed to docker hub.

### Images
- [filipstenbeck/note-app](https://hub.docker.com/r/filipstenbeck/note-app/tags)
- [filipstenbeck/note-app-api](https://hub.docker.com/r/filipstenbeck/note-app-api/tags)

There is a **docker-compose.yaml** file in this repository that can be used to start **both** services:

Clone the repository:
```sh
git clone git@github.com:FilipStenbeck/note-app.git
```
From within the project folder:
```sh
docker-compose up
```
Point your favorite browser to http://localhost:3000. The database has a few notes prepoulated, so there is something to look at the first time the application is started.

## Development
Install and run in the app in development mode:

```sh
yarn
yarn dev
```

**Important** The app requires that the backend API is up and running to work. Before starting make sure that the API is up.

### Configuration

For convinience, all needed environment variables is commited in a _.env_ file (I would not do that in a real project)

### ENVIRONMENT variables
The following environment variables is used in the application

- **REACT_APP_API_ROOT** : url to API root (Example http://localhost:4000)
- **REACT_APP_ROOT** : url to APP root  (Example http://localhost:3000)

## Test
There are som test included, to run test:

```sh
yarn test
```

## Production

Below is the details on how to build and run the application in production mode

## Build

To make a production optimized build:

```sh
yarn build
```

## Run

To run the application using the production ready build and serve it using the included node.js express server. 

```sh
yarn start
```
When running the application with _yarn start_ the ENVIRONMENT variables are set to default values.

## Docker

Build a docker image from the _Dockerfile_ included.
To start both the app and the needed api. First make sure you have built **both** docker images. Instruction on how to build the docker for the [**API**](https://github.com/FilipStenbeck/note-app-api)

The following command can be used to create a docker image of the app:

```sh
yarn docker:build
```
Once *both* docker images are built, start both the *app* and *api* by running:

```sh
docker-compose up
```
When running the application with _docker-compose_ the ENVIRONMENT variables are picked up from the **.env** file


