import { Socket } from "socket.io";
import { M, Marshaller } from "@zensors/sheriff";

import { Challenge } from "./challenge";

export interface JobRequest {
  url: string;
}

export namespace JobRequest {
  export const Marshaller: Marshaller<JobRequest> = M.obj({
    url: M.str,
  });
}

export type SocketState =
  | { kind: SocketState.Kind.Waiting }
  | {
      kind: SocketState.Kind.Challenge;
      request: JobRequest;
      challenge: Challenge;
    }
  | { kind: SocketState.Kind.Queued; request: JobRequest; jobUid: string }
  | {
      kind: SocketState.Kind.Accepted;
      request: JobRequest;
      launchingAt: number;
    }
  | {
      kind: SocketState.Kind.Processing;
      request: JobRequest;
      until: number;
    };

export namespace SocketState {
  export enum Kind {
    Waiting,
    Challenge,
    Queued,
    Accepted,
    Processing,
  }
}

export interface SocketWithState extends Socket {
  state: SocketState;
}
