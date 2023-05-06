import { HoldPurpose } from "./HoldPurpose.js";
import { SystemKind } from "./SystemKind.js";

export type SystemState =
	| SystemState.Movement
	| SystemState.Settings
	| SystemState.Reset
	| SystemState.Vent
	| SystemState.Meeting
	| SystemState.EmergencyButton
	| SystemState.FileTransfer
	| SystemState.ProcessSample
	| SystemState.ProvideCredentials
	| SystemState.PurchaseSnack
	| SystemState.RecalibrateEngine
	| SystemState.Conspiracy
	| SystemState.Hold
	| SystemState.Satellite
	;

export namespace SystemState {
	interface Base<K extends SystemKind> {
		kind: K;
		id: number;
		devices: string[];
	}

	export interface Movement extends Base<SystemKind.Movement> {}

	export interface Settings extends Base<SystemKind.Settings> {}

	export interface Reset extends Base<SystemKind.Reset> {}

	export interface Vent extends Base<SystemKind.Vent> {
		devices: string[];
	}

	export interface Meeting extends Base<SystemKind.Meeting> {
		calledBy: string;
		trigger: { kind: "emergency" } | { kind: "body"; body: string };
		votesSubmitted: string[];
	}

	export interface EmergencyButton extends Base<SystemKind.EmergencyButton> {}

	export interface FileTransfer extends Base<SystemKind.FileTransfer> {
		downloadComplete: boolean;
		uploadComplete: boolean;
	}

	export interface ProcessSample extends Base<SystemKind.ProcessSample> {
		timerEndsAt?: number;
		taskComplete: boolean;
		role: "begin" | "end";
	}

	export interface ProvideCredentials extends Base<SystemKind.ProvideCredentials> {
		credentials: {
			username: string;
			password: string;
		};
		complete: boolean;
	}

	export interface PurchaseSnack extends Base<SystemKind.PurchaseSnack> {
		desiredSnack: string;
		complete: boolean;
	}

	export interface RecalibrateEngine extends Base<SystemKind.RecalibrateEngine> {
		complete: boolean;
	}

	export interface Conspiracy extends Base<SystemKind.Conspiracy> {}

	export interface Satellite extends Base<SystemKind.Satellite> {}

	export interface Hold extends Base<SystemKind.Hold> {
		until: number;
		purpose: HoldPurpose.AsJson;
	}
}
