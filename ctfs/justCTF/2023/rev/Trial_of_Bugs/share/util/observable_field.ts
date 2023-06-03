type ObservableFieldCallback<T> = (newValue: T, oldValue: T) => void;

export class ObservableField<T> {
    private value: T;
    private callbacks: ObservableFieldCallback<T>[] = [];

    constructor(value: T) {
        this.value = value;
    }

    get(): T {
        return this.value;
    }

    set(value: T) {
        const oldValue = this.value;
        this.value = value;
        for (const cb of this.callbacks)
            cb(value, oldValue);
    }

    addCallback(cb: ObservableFieldCallback<T>) {
        this.callbacks.push(cb);
    }

    removeCallback(cb: ObservableFieldCallback<T>) {
        const iof = this.callbacks.indexOf(cb);
        if (iof !== -1)
            this.callbacks.splice(iof, 1);
    }
}
