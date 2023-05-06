import { SystemKind, SystemState } from "@amongst/game-common";

import { ConspiracyController } from "./ConspiracyController.js";
import { EmergencyButtonController } from "./EmergencyButtonController.js";
import { FileTransferController } from "./FileTransferController.js";
import { HoldController } from "./HoldController.js";
import { MeetingController } from "./MeetingController.js";
import { MovementController } from "./MovementController.js";
import { ProcessSampleController } from "./ProcessSampleController.js";
import { ProvideCredentialsController } from "./ProvideCredentialsController.js";
import { PurchaseSnackController } from "./PurchaseSnackController.js";
import { RecalibrateEngineController } from "./RecalibrateEngineController.js";
import { ResetController } from "./ResetController.js";
import { SatelliteController } from "./SatelliteController.js";
import { SettingsController } from "./SettingsController.js";
import { VentController } from "./VentController.js";

export type Controller =
	| MovementController
	| SettingsController
	| ResetController
	| VentController
	| MeetingController
	| EmergencyButtonController
	| FileTransferController
	| ProcessSampleController
	| ProvideCredentialsController
	| PurchaseSnackController
	| RecalibrateEngineController
	| ConspiracyController
	| HoldController
	| SatelliteController
	;

export function getController(system: SystemState): Controller {
	switch (system.kind) {
		case SystemKind.Movement: return new MovementController();
		case SystemKind.Settings: return new SettingsController();
		case SystemKind.Reset: return new ResetController();
		case SystemKind.Vent: return new VentController(system);
		case SystemKind.Meeting: return new MeetingController(system);
		case SystemKind.EmergencyButton: return new EmergencyButtonController();
		case SystemKind.FileTransfer: return new FileTransferController(system);
		case SystemKind.ProcessSample: return new ProcessSampleController(system);
		case SystemKind.ProvideCredentials: return new ProvideCredentialsController(system);
		case SystemKind.PurchaseSnack: return new PurchaseSnackController(system);
		case SystemKind.RecalibrateEngine: return new RecalibrateEngineController(system);
		case SystemKind.Conspiracy: return new ConspiracyController(system);
		case SystemKind.Hold: return new HoldController(system);
		case SystemKind.Satellite: return new SatelliteController(system);
	}
}

export { ConspiracyController } from "./ConspiracyController.js";
export { EmergencyButtonController } from "./EmergencyButtonController.js";
export { FileTransferController } from "./FileTransferController.js";
export { HoldController } from "./HoldController.js";
export { MeetingController } from "./MeetingController.js";
export { MovementController } from "./MovementController.js";
export { ProcessSampleController } from "./ProcessSampleController.js";
export { ProvideCredentialsController } from "./ProvideCredentialsController.js";
export { PurchaseSnackController } from "./PurchaseSnackController.js";
export { RecalibrateEngineController } from "./RecalibrateEngineController.js";
export { ResetController } from "./ResetController.js";
export { SatelliteController } from "./SatelliteController.js";
export { SettingsController } from "./SettingsController.js";
export { VentController } from "./VentController.js";
