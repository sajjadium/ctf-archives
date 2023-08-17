# Note API

## Overview

This is the backend API for [**The Note taking application**](https://github.com/FilipStenbeck/note-app)the note taking application. Implemented features are

-   Save notes in database
-   update notes in database
-   Delete notes from the database


### Architecture

The applications consist of a **Apollo GraphQL** application and a [**React application**](https://github.com/FilipStenbeck/note-app). This is tha API. It stores/fetches notes from a very simple dile based database (I would not use this kind of DB in anything real)


### Dependencies (major)

List of major libraries and tools:

-   [Apollo GraphQL](https://github.com/apollographql)
-   [node-json-db](https://github.com/Belphemur/node-json-db)

## How to use

Install it and run in dev mode:

```sh
yarn
yarn dev
```


## Production

Below is the detail run the application in production.

### Run

To start the application: 

```sh
yarn start
```

## Docker

Build a docker image from the _Dockerfile_ included.
To start both the app and the needed api. First make sure you have built **both** docker images. Instruction on how to build the docker for the [**App**](https://github.com/FilipStenbeck/note-app)

The following command can be used to create a docker image of the api:

```sh
yarn docker:build
```
Once *both* docker images is built, start both the *app* and *api* by using docker-compose in the [**App**](https://github.com/FilipStenbeck/note-app):

```sh
docker-compose up
```

