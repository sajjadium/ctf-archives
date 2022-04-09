export interface ClientEvent {
	join: () => void;
	action: (action: TickAction) => void;
	interact: (body: unknown) => void;
	requestSync: () => void;
	ping: (ack: () => void) => void;
}

export interface TickAction {
	syncId: number;
	tick: number;
	action: unknown;
}
