import { Socket } from "socket.io";
import { M, Marshaller } from "@zensors/sheriff";

import { Challenge } from "./challenge";

export interface JobRequest {
	url: string;
}

export namespace JobRequest {
	export const Marshaller: Marshaller<JobRequest> = M.obj({
		url: M.str
	});
}

export interface JobResponse {
	targetIp: string;
	sensorPort: number;
	sensorToken: string;
}

export type SocketState =
	| { kind: SocketState.Kind.Waiting }
	| { kind: SocketState.Kind.Challenge, request: JobRequest, challenge: Challenge }
	| { kind: SocketState.Kind.Queued, request: JobRequest, jobUid: string }
	| { kind: SocketState.Kind.Accepted, request: JobRequest, response: JobResponse, launchingAt: number }
	| { kind: SocketState.Kind.Processing, request: JobRequest, response: JobResponse, until: number }
	;

export namespace SocketState {
	export enum Kind {
		Waiting,
		Challenge,
		Queued,
		Accepted,
		Processing
	}
}

export interface SocketWithState extends Socket {
	state: SocketState;
}
