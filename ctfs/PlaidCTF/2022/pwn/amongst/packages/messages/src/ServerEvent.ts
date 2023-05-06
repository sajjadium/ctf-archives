import { Map } from "immutable";

import { Color, PlayerVisualState, SystemState } from "@amongst/game-common";
import { Point } from "@amongst/geometry";

export interface ServerEvent {
	sync: (sync: GameSync) => void;
	update: (bundle: GameUpdateBundle) => void;
}

export interface LevelSync {
	map: string;
	systems: SystemState[];
}

export interface GameSync {
	id: number;
	tick: number;
	partialTick: number;
	nextPlayableTick: number;
	self: {
		id: string;
		name: string;
		color: Color;
		location: Point.AsJson;
		visualState: PlayerVisualState;
		system: number;
		dead: boolean;
		hoaxer: boolean;
		emergencyMeetings: number;
	};
	others: {
		id: string;
		name: string;
		color: Color;
	}[];
	level: LevelSync;
}

export interface GameUpdateBundle {
	tick: number;
	partialTick: number;
	updates: GameUpdate.AsJson[];
}

export type GameUpdate =
	| GameUpdate.PlayerJoined
	| GameUpdate.PlayerChangedSettings
	| GameUpdate.PlayerLeft
	| GameUpdate.VisibilityUpdate
	| GameUpdate.SystemStateUpdate
	| GameUpdate.FileDownloadPacket
	| GameUpdate.ProcessSampleDisplayUpdate
	| GameUpdate.ProvideCredentialsResponse
	| GameUpdate.PurchaseSnackLayoutReady
	| GameUpdate.PurchaseSnackOutput
	| GameUpdate.RecalibrateEngineUpdate
	| GameUpdate.ConspiracyUpdate
	| GameUpdate.SatelliteUpdate
	;

export namespace GameUpdate {
	export enum Kind {
		PlayerJoined = "PlayerJoined",
		PlayerChangedSettings = "PlayerChangedSettings",
		PlayerLeft = "PlayerLeft",
		VisibilityUpdate = "VisibilityUpdate",
		SystemStateUpdate = "SystemStateUpdate",
		FileDownloadPacket = "FileDownloadPacket",
		ProcessSampleDisplayUpdate = "ProcessSampleDisplayUpdate",
		ProvideCredentialsResponse = "ProvideCredentialsResponse",
		PurchaseSnackLayoutReady = "PurchaseSnackLayoutReady",
		PurchaseSnackOutput = "PurchaseSnackOutput",
		RecalibrateEngineUpdate = "RecalibrateEngineUpdate",
		ConspiracyUpdate = "ConspiracyUpdate",
		SatelliteUpdate = "SatelliteUpdate",
	}

	export type AsJson =
		| PlayerJoined.AsJson
		| PlayerChangedSettings.AsJson
		| PlayerLeft.AsJson
		| VisibilityUpdate.AsJson
		| SystemStateUpdate.AsJson
		| FileDownloadPacket.AsJson
		| ProcessSampleDisplayUpdate.AsJson
		| ProvideCredentialsResponse.AsJson
		| PurchaseSnackLayoutReady.AsJson
		| PurchaseSnackOutput.AsJson
		| RecalibrateEngineUpdate.AsJson
		| ConspiracyUpdate.AsJson
		| SatelliteUpdate.AsJson
		;

	export function fromJson(json: AsJson): GameUpdate {
		switch (json.kind) {
			case Kind.PlayerJoined: return PlayerJoined.fromJson(json);
			case Kind.PlayerChangedSettings: return PlayerChangedSettings.fromJson(json);
			case Kind.PlayerLeft: return PlayerLeft.fromJson(json);
			case Kind.VisibilityUpdate: return VisibilityUpdate.fromJson(json);
			case Kind.SystemStateUpdate: return SystemStateUpdate.fromJson(json);
			case Kind.FileDownloadPacket: return FileDownloadPacket.fromJson(json);
			case Kind.ProcessSampleDisplayUpdate: return ProcessSampleDisplayUpdate.fromJson(json);
			case Kind.ProvideCredentialsResponse: return ProvideCredentialsResponse.fromJson(json);
			case Kind.PurchaseSnackLayoutReady: return PurchaseSnackLayoutReady.fromJson(json);
			case Kind.PurchaseSnackOutput: return PurchaseSnackOutput.fromJson(json);
			case Kind.RecalibrateEngineUpdate: return RecalibrateEngineUpdate.fromJson(json);
			case Kind.ConspiracyUpdate: return ConspiracyUpdate.fromJson(json);
			case Kind.SatelliteUpdate: return SatelliteUpdate.fromJson(json);
		}
	}

	export class PlayerJoined {
		public readonly kind = Kind.PlayerJoined;
		public readonly id: string;
		public readonly name: string;
		public readonly color: Color;

		public constructor(args: PlayerJoined.ConstructorArgs) {
			this.id = args.id;
			this.name = args.name;
			this.color = args.color;
		}

		public static fromJson(json: PlayerJoined.AsJson): PlayerJoined {
			return new PlayerJoined({
				id: json.id,
				name: json.name,
				color: json.color,
			});
		}

		public toJson(): PlayerJoined.AsJson {
			return {
				kind: Kind.PlayerJoined,
				id: this.id,
				name: this.name,
				color: this.color,
			};
		}
	}

	export namespace PlayerJoined {
		export interface ConstructorArgs {
			id: string;
			name: string;
			color: Color;
		}

		export interface AsJson {
			kind: Kind.PlayerJoined;
			id: string;
			name: string;
			color: Color;
		}
	}

	export class PlayerChangedSettings {
		public readonly kind = Kind.PlayerChangedSettings;
		public readonly id: string;
		public readonly name: string;
		public readonly color: Color;

		public constructor(args: PlayerChangedSettings.ConstructorArgs) {
			this.id = args.id;
			this.name = args.name;
			this.color = args.color;
		}

		public static fromJson(json: PlayerChangedSettings.AsJson): PlayerChangedSettings {
			return new PlayerChangedSettings({
				id: json.id,
				name: json.name,
				color: json.color,
			});
		}

		public toJson(): PlayerChangedSettings.AsJson {
			return {
				kind: Kind.PlayerChangedSettings,
				id: this.id,
				name: this.name,
				color: this.color,
			};
		}
	}

	export namespace PlayerChangedSettings {
		export interface ConstructorArgs {
			id: string;
			name: string;
			color: Color;
		}

		export interface AsJson {
			kind: Kind.PlayerChangedSettings;
			id: string;
			name: string;
			color: Color;
		}
	}

	export class PlayerLeft {
		public readonly kind = Kind.PlayerLeft;
		public readonly id: string;

		public constructor(args: PlayerLeft.ConstructorArgs) {
			this.id = args.id;
		}

		public static fromJson(json: PlayerLeft.AsJson): PlayerLeft {
			return new PlayerLeft({
				id: json.id,
			});
		}

		public toJson(): PlayerLeft.AsJson {
			return {
				kind: Kind.PlayerLeft,
				id: this.id,
			};
		}
	}

	export namespace PlayerLeft {
		export interface ConstructorArgs {
			id: string;
		}

		export interface AsJson {
			kind: Kind.PlayerLeft;
			id: string;
		}
	}

	export class VisibilityUpdate {
		public readonly kind = Kind.VisibilityUpdate;
		public readonly players: VisibilityUpdate.Player[];
		public readonly bodies: VisibilityUpdate.Body[];

		public constructor(args: VisibilityUpdate.ConstructorArgs) {
			this.players = args.players;
			this.bodies = args.bodies;
		}

		public static fromJson(json: VisibilityUpdate.AsJson): VisibilityUpdate {
			return new VisibilityUpdate({
				players: json.players.map(VisibilityUpdate.Player.fromJson),
				bodies: json.bodies.map(VisibilityUpdate.Body.fromJson),
			});
		}

		public toJson(): VisibilityUpdate.AsJson {
			return {
				kind: Kind.VisibilityUpdate,
				players: this.players.map((p) => p.toJson()),
				bodies: this.bodies.map((b) => b.toJson()),
			};
		}
	}

	export namespace VisibilityUpdate {
		export interface ConstructorArgs {
			players: Player[];
			bodies: Body[];
		}

		export interface AsJson {
			kind: Kind.VisibilityUpdate;
			players: Player.AsJson[];
			bodies: Body.AsJson[];
		}

		export class Player {
			public readonly id: string;
			public readonly location: Point;
			public readonly visualState: PlayerVisualState;
			public readonly dead?: boolean;
			public readonly hoaxer?: boolean;

			public constructor(args: Player.ConstructorArgs) {
				this.id = args.id;
				this.location = args.location;
				this.visualState = args.visualState;
				this.dead = args.dead;
				this.hoaxer = args.hoaxer;
			}

			public static fromJson(json: Player.AsJson): Player {
				return new Player({
					id: json.id,
					location: Point.fromJson(json.location),
					visualState: json.visualState,
					dead: json.dead,
					hoaxer: json.hoaxer,
				});
			}

			public toJson(): Player.AsJson {
				return {
					id: this.id,
					location: this.location.toJson(),
					visualState: this.visualState,
					dead: this.dead,
					hoaxer: this.hoaxer,
				};
			}
		}

		export namespace Player {
			export interface ConstructorArgs {
				id: string;
				location: Point;
				visualState: PlayerVisualState;
				dead?: boolean;
				hoaxer?: boolean;
			}

			export interface AsJson {
				id: string;
				location: Point.AsJson;
				visualState: PlayerVisualState;
				dead?: boolean;
				hoaxer?: boolean;
			}
		}

		export class Body {
			public readonly id: string;
			public readonly color: Color;
			public readonly location: Point;

			public constructor(args: Body.ConstructorArgs) {
				this.id = args.id;
				this.color = args.color;
				this.location = args.location;
			}

			public static fromJson(json: Body.AsJson): Body {
				return new Body({
					id: json.id,
					color: json.color,
					location: Point.fromJson(json.location),
				});
			}

			public toJson(): Body.AsJson {
				return {
					id: this.id,
					color: this.color,
					location: this.location.toJson(),
				};
			}
		}

		export namespace Body {
			export interface ConstructorArgs {
				id: string;
				color: Color;
				location: Point;
			}

			export interface AsJson {
				id: string;
				color: Color;
				location: Point.AsJson;
			}
		}
	}

	export class SystemStateUpdate {
		public readonly kind = Kind.SystemStateUpdate;
		public readonly state: SystemState;

		public constructor(args: SystemStateUpdate.ConstructorArgs) {
			this.state = args.state;
		}

		public static fromJson(json: SystemStateUpdate.AsJson): SystemStateUpdate {
			return new SystemStateUpdate({
				state: json.state,
			});
		}

		public toJson(): SystemStateUpdate.AsJson {
			return {
				kind: Kind.SystemStateUpdate,
				state: this.state,
			};
		}
	}

	export namespace SystemStateUpdate {
		export interface ConstructorArgs {
			state: SystemState;
		}

		export interface AsJson {
			kind: Kind.SystemStateUpdate;
			state: SystemState;
		}
	}

	export class FileDownloadPacket {
		public readonly kind = Kind.FileDownloadPacket;
		public readonly id: number;
		public readonly position: number;
		public readonly totalSize: number;
		public readonly data: string;

		public constructor(args: FileDownloadPacket.ConstructorArgs) {
			this.id = args.id;
			this.position = args.position;
			this.totalSize = args.totalSize;
			this.data = args.data;
		}

		public static fromJson(json: FileDownloadPacket.AsJson): FileDownloadPacket {
			return new FileDownloadPacket({
				id: json.id,
				position: json.position,
				totalSize: json.totalSize,
				data: json.data
			});
		}

		public toJson(): FileDownloadPacket.AsJson {
			return {
				kind: Kind.FileDownloadPacket,
				id: this.id,
				position: this.position,
				totalSize: this.totalSize,
				data: this.data
			};
		}
	}

	export namespace FileDownloadPacket {
		export interface ConstructorArgs {
			id: number;
			position: number;
			totalSize: number;
			data: string;
		}

		export interface AsJson {
			kind: Kind.FileDownloadPacket;
			id: number;
			position: number;
			totalSize: number;
			data: string;
		}
	}

	export class ProcessSampleDisplayUpdate {
		public readonly kind = Kind.ProcessSampleDisplayUpdate;
		public readonly content: string;

		public constructor(args: ProcessSampleDisplayUpdate.ConstructorArgs) {
			this.content = args.content;
		}

		public static fromJson(json: ProcessSampleDisplayUpdate.AsJson): ProcessSampleDisplayUpdate {
			return new ProcessSampleDisplayUpdate({
				content: json.content,
			});
		}

		public toJson(): ProcessSampleDisplayUpdate.AsJson {
			return {
				kind: Kind.ProcessSampleDisplayUpdate,
				content: this.content,
			};
		}
	}

	export namespace ProcessSampleDisplayUpdate {
		export interface ConstructorArgs {
			content: string;
		}

		export interface AsJson {
			kind: Kind.ProcessSampleDisplayUpdate;
			content: string;
		}
	}

	export class ProvideCredentialsResponse {
		public readonly kind = Kind.ProvideCredentialsResponse;
		public readonly success: boolean;
		public readonly message: string;

		public constructor(args: ProvideCredentialsResponse.ConstructorArgs) {
			this.success = args.success;
			this.message = args.message;
		}

		public static fromJson(json: ProvideCredentialsResponse.AsJson): ProvideCredentialsResponse {
			return new ProvideCredentialsResponse({
				success: json.success,
				message: json.message,
			});
		}

		public toJson(): ProvideCredentialsResponse.AsJson {
			return {
				kind: Kind.ProvideCredentialsResponse,
				success: this.success,
				message: this.message,
			};
		}
	}

	export namespace ProvideCredentialsResponse {
		export interface ConstructorArgs {
			success: boolean;
			message: string;
		}

		export interface AsJson {
			kind: Kind.ProvideCredentialsResponse;
			success: boolean;
			message: string;
		}
	}

	export class PurchaseSnackLayoutReady {
		public readonly kind = Kind.PurchaseSnackLayoutReady;
		public readonly layout: Map<string, string>;

		public constructor(args: PurchaseSnackLayoutReady.ConstructorArgs) {
			this.layout = args.layout;
		}

		public static fromJson(json: PurchaseSnackLayoutReady.AsJson): PurchaseSnackLayoutReady {
			return new PurchaseSnackLayoutReady({
				layout: Map(json.layout),
			});
		}

		public toJson(): PurchaseSnackLayoutReady.AsJson {
			return {
				kind: Kind.PurchaseSnackLayoutReady,
				layout: this.layout.toJSON(),
			};
		}
	}

	export namespace PurchaseSnackLayoutReady {
		export interface ConstructorArgs {
			layout: Map<string, string>;
		}

		export interface AsJson {
			kind: Kind.PurchaseSnackLayoutReady;
			layout: Record<string, string>;
		}
	}

	export class PurchaseSnackOutput {
		public readonly kind = Kind.PurchaseSnackOutput;
		public readonly event: "display" | "dispense";
		public readonly body: string;

		public constructor(args: PurchaseSnackOutput.ConstructorArgs) {
			this.event = args.event;
			this.body = args.body;
		}

		public static fromJson(json: PurchaseSnackOutput.AsJson): PurchaseSnackOutput {
			return new PurchaseSnackOutput({
				event: json.event,
				body: json.body,
			});
		}

		public toJson(): PurchaseSnackOutput.AsJson {
			return {
				kind: Kind.PurchaseSnackOutput,
				event: this.event,
				body: this.body,
			};
		}
	}

	export namespace PurchaseSnackOutput {
		export interface ConstructorArgs {
			event: "display" | "dispense";
			body: string;
		}

		export interface AsJson {
			kind: Kind.PurchaseSnackOutput;
			event: "display" | "dispense";
			body: string;
		}
	}

	export class RecalibrateEngineUpdate {
		public readonly kind = Kind.RecalibrateEngineUpdate;
		public readonly event: "display" | "flash";
		public readonly body: string;

		public constructor(args: RecalibrateEngineUpdate.ConstructorArgs) {
			this.event = args.event;
			this.body = args.body;
		}

		public static fromJson(json: RecalibrateEngineUpdate.AsJson): RecalibrateEngineUpdate {
			return new RecalibrateEngineUpdate({
				event: json.event,
				body: json.body,
			});
		}

		public toJson(): RecalibrateEngineUpdate.AsJson {
			return {
				kind: Kind.RecalibrateEngineUpdate,
				event: this.event,
				body: this.body,
			};
		}
	}

	export namespace RecalibrateEngineUpdate {
		export interface ConstructorArgs {
			event: "display" | "flash";
			body: string;
		}

		export interface AsJson {
			kind: Kind.RecalibrateEngineUpdate;
			event: "display" | "flash";
			body: string;
		}
	}

	export class ConspiracyUpdate {
		public readonly kind = Kind.ConspiracyUpdate;
		public readonly flags: string[];

		public constructor(args: ConspiracyUpdate.ConstructorArgs) {
			this.flags = args.flags;
		}

		public static fromJson(json: ConspiracyUpdate.AsJson): ConspiracyUpdate {
			return new ConspiracyUpdate({
				flags: json.flags,
			});
		}

		public toJson(): ConspiracyUpdate.AsJson {
			return {
				kind: Kind.ConspiracyUpdate,
				flags: this.flags,
			};
		}
	}

	export namespace ConspiracyUpdate {
		export interface ConstructorArgs {
			flags: string[];
		}

		export interface AsJson {
			kind: Kind.ConspiracyUpdate;
			flags: string[];
		}
	}

	export class SatelliteUpdate {
		public readonly kind = Kind.SatelliteUpdate;
		public readonly flags: string[];

		public constructor(args: SatelliteUpdate.ConstructorArgs) {
			this.flags = args.flags;
		}

		public static fromJson(json: SatelliteUpdate.AsJson): SatelliteUpdate {
			return new SatelliteUpdate({
				flags: json.flags,
			});
		}

		public toJson(): SatelliteUpdate.AsJson {
			return {
				kind: Kind.SatelliteUpdate,
				flags: this.flags,
			};
		}
	}

	export namespace SatelliteUpdate {
		export interface ConstructorArgs {
			flags: string[];
		}

		export interface AsJson {
			kind: Kind.SatelliteUpdate;
			flags: string[];
		}
	}
}
