import { Worker } from "cluster";
import EventEmitter from "events";

namespace IpcWrapper {
	export enum Kind {
		Request = "Request",
		Response = "Response",
	}

	export interface Request<T> {
		kind: Kind.Request;
		id: number;
		body: T;
	}

	export interface Response<T> {
		kind: Kind.Response;
		id: number;
		body: T;
	}
}

type IncomingMessage<SelfRequest, OtherResponse> = IpcWrapper.Request<SelfRequest> | IpcWrapper.Response<OtherResponse>;

export abstract class IpcHandler<SelfRequest, SelfResponse, OtherRequest, OtherResponse> {
	private responseEmitter: EventEmitter;
	private nextRequestId: number;

	public constructor() {
		this.responseEmitter = new EventEmitter();
		this.nextRequestId = 0;
	}

	public start() {
		this.setIpcListener(async (worker: Worker, message: IncomingMessage<SelfRequest, OtherResponse>) => {
			switch (message.kind) {
				case IpcWrapper.Kind.Request: {
					const response = await this.handleRequest(worker, message.body);
					this.sendResponse(worker, message.id, response);
					break;
				}

				case IpcWrapper.Kind.Response: {
					this.responseEmitter.emit("response", message.id, message.body);
				}
			}
		});
	}

	protected async sendRequest<T extends OtherRequest>(worker: Worker, body: T): Promise<OtherResponse> {
		const requestId = this.nextRequestId;
		this.nextRequestId++;

		const wrappedRequest: IpcWrapper.Request<T> = {
			kind: IpcWrapper.Kind.Request,
			id: requestId,
			body
		};

		worker.send(wrappedRequest);

		return new Promise((resolve) => {
			const onResponse = (id: number, response: OtherResponse) => {
				if (id === requestId) {
					this.responseEmitter.removeListener("response", onResponse);
					resolve(response);
				}
			};

			this.responseEmitter.on("response", onResponse);
		});
	}

	private async sendResponse(worker: Worker, id: number, body: SelfResponse) {
		const wrappedResponse: IpcWrapper.Response<SelfResponse> = {
			kind: IpcWrapper.Kind.Response,
			id,
			body
		};

		worker.send(wrappedResponse);
	}

	protected abstract setIpcListener(
		fn: (worker: Worker, request: IncomingMessage<SelfRequest, OtherResponse>) => void
	): void;
	protected abstract handleRequest(worker: Worker, request: SelfRequest): Promise<SelfResponse>;
}
