import { ApolloClient, ApolloProvider, InMemoryCache } from "@apollo/client";
import { createPersistedQueryLink } from "@apollo/client/link/persisted-queries";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { CssBaseline } from "@mui/material";
import createUploadLink from "apollo-upload-client/createUploadLink.mjs";
import { sha256 } from "crypto-hash";
import { SnackbarProvider } from "notistack";
import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import "./main.css";
import { CreateStoryPage } from "./pages/CreateStoryPage/CreateStoryPage";
import { ExportDetailsPage } from "./pages/ExportDetailsPage/ExportDetailsPage";
import { ExportListPage } from "./pages/ExportListPage/ExportListPage";
import { ExportStoryPage } from "./pages/ExportStoryPage/ExportStoryPage";
import { ListStoriesPage } from "./pages/ListStoriesPage/ListStoriesPage";
import { Render } from "./pages/Render/Render";
import { UploadAssetPage } from "./pages/UploadAssetPage/UploadAssetPage";
import { ViewStoryPage } from "./pages/ViewStoryPage/ViewStoryPage";


const linkChain = createPersistedQueryLink({ sha256 }).concat(
  createUploadLink({
    uri: "/api/graphql",
    credentials: "include",
  }),
);

const client = new ApolloClient({
  cache: new InMemoryCache(),
  link: linkChain,
});

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { path: "/new", element: <CreateStoryPage /> },
      {
        path: "/stories/:id",
        element: <ViewStoryPage />,
      },
      { path: "/exports", element: <ExportListPage /> },
      { path: "/export", element: <ExportStoryPage /> },
      { path: "/export/:id", element: <ExportDetailsPage /> },
      { path: "/upload", element: <UploadAssetPage /> },
      { path: "", element: <ListStoriesPage /> },
    ],
  },
  {
    path: "/render/:id",
    element: <Render />,
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ApolloProvider client={client}>
      <CssBaseline>
        <SnackbarProvider
          maxSnack={3}
          anchorOrigin={{
            vertical: "top",
            horizontal: "center",
          }}
        >
          <RouterProvider router={router} />
        </SnackbarProvider>
      </CssBaseline>
    </ApolloProvider>
  </React.StrictMode>,
);
