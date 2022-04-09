export namespace IpcMessage {
	export namespace Worker {
		export enum Kind {
			CreateGame = "CreateGame",
			GetPort = "GetPort",
		}

		export type Request = Request.CreateGame | Request.GetPort;

		export namespace Request {
			export interface CreateGame {
				kind: Kind.CreateGame;
				id: string;
			}

			export interface GetPort {
				kind: Kind.GetPort;
			}
		}

		export type Response = Response.CreateGame | Response.GetPort;

		export namespace Response {
			export interface CreateGame {
				kind: Kind.CreateGame;
				id: string;
				port: number;
			}

			export interface GetPort {
				kind: Kind.GetPort;
				port: number;
			}
		}

		export type ResponseFor<T extends Request> =
			T extends Request.CreateGame ? Response.CreateGame :
			never;
	}

	export namespace Primary {
		export enum Kind {
			CloseGame = "CloseGame",
		}

		export type Request = Request.CloseGame;

		export namespace Request {
			export interface CloseGame {
				kind: Kind.CloseGame;
				id: string;
			}
		}

		export type Response = Response.CloseGame;

		export namespace Response {
			export interface CloseGame {
				kind: Kind.CloseGame;
			}
		}

		export type ResponseFor<T extends Request> =
			T extends Request.CloseGame ? Response.CloseGame :
			never;
	}
}
