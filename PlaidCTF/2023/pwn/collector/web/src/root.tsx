// @refresh reload
import { Show, Suspense } from "solid-js";
import {
  A,
  Body,
  createRouteAction,
  createRouteData,
  ErrorBoundary,
  FileRoutes,
  Head,
  Html,
  Meta,
  Routes,
  Scripts,
  Title,
  useRouteData,
} from "solid-start";
import { Toaster } from "solid-toast";
import "./root.css";

export default function Root() {
  return (
    <Html lang="en">
      <Head>
        <Title>Loot Collector</Title>
        <Meta charset="utf-8" />
        <Meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <Body>
        <ErrorBoundary>
          <div class="main-header">
            <nav class="topbar-navigation">
              <A class="nav-button" href="/" end={true} activeClass="active">
                Marketplace
              </A>
              <A class="nav-button" href="/scoreboard" activeClass="active">
                Scoreboard
              </A>
              <A class="nav-button" href="/private" activeClass="active">
                Private
              </A>
              <div class="spacer"></div>
            </nav>
          </div>
          <Suspense fallback={<div>Loading</div>}>
            <Routes>
              <FileRoutes />
            </Routes>
          </Suspense>
          <Toaster />
        </ErrorBoundary>
        <Scripts />
      </Body>
    </Html>
  );
}
