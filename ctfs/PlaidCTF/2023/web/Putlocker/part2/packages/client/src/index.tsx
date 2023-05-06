import { ApolloProvider } from "@apollo/client";
import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { client } from "./apollo";
import { CreateEpisode } from "./views/CreateEpisode";
import { CreatePlaylist } from "./views/CreatePlaylist";
import { CreateShow } from "./views/CreateShow";
import { EditEpisode } from "./views/EditEpisode";
import { EditShow } from "./views/EditShow";
import { Episode } from "./views/Episode";
import { Genre } from "./views/Genre";
import { Home } from "./views/Home";
import { Login } from "./views/Login";
import { Playlist } from "./views/Playlist";
import { Register } from "./views/Register";
import { Show } from "./views/Show";
import { User } from "./views/User";

import "./index.scss";

const root = createRoot(document.getElementById("root")!);
root.render(
	<ApolloProvider client={client}>
		<BrowserRouter>
			<Routes>
				<Route path="/" Component={Home} />
				<Route path="/login" Component={Login} />
				<Route path="/register" Component={Register} />
				<Route path="/show/create" Component={CreateShow} />
				<Route path="/show/:id" Component={Show} />
				<Route path="/show/:id/edit" Component={EditShow} />
				<Route path="/episode/create" Component={CreateEpisode} />
				<Route path="/episode/:id" Component={Episode} />
				<Route path="/episode/:id/edit" Component={EditEpisode} />
				<Route path="/playlist/:id" Component={Playlist} />
				<Route path="/playlist/create" Component={CreatePlaylist} />
				<Route path="/genre/:id" Component={Genre} />
				<Route path="/user/:id" Component={User} />
				<Route path="*" element={<Navigate to="/" replace />} />
			</Routes>
		</BrowserRouter>
	</ApolloProvider>
);
