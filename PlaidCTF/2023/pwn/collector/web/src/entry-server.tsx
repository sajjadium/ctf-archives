import { FetchEvent, FormError, ResponseError, ServerError } from "solid-start";
import {
  Middleware,
  StartServer,
  createHandler,
  renderAsync,
} from "solid-start/entry-server";

const requiredHost: string | undefined = process.env.HOST;

const rejectInvalidHosts: Middleware = ({ forward }) => {
  if (!requiredHost) {
    return forward;
  }

  else {
    return (event: FetchEvent) => {
      const host = event.request.headers.get('Host');
      const hostname = host?.split(':', 2)?.[0];
      if (hostname !== requiredHost) {
        return new Response("Invalid host", { status: 403 });
      }
      return forward(event);
    }
  }
}

export default createHandler(
  rejectInvalidHosts,
  renderAsync((event) => <StartServer event={event} />)
);
