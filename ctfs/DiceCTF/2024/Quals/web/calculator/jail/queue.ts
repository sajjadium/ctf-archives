class SignalQueue {
    queue: Array<Function>
    constructor() { this.queue = [] }
    wait() { return new Promise((resolve) => { this.queue.push(resolve) }) }
    signal() {
        if (this.queue.length > 0) {
            const resolve = this.queue.shift()!
            resolve()
        }
    }
}

export class ResourceCluster<T> {
    free: T[]
    signals: SignalQueue
    constructor(resources: T[]) {
        this.free = resources
        this.signals = new SignalQueue()
    }

    async queue<U>(callback: (resource: T) => Promise<U>) {
        while (this.free.length === 0) {
            await this.signals.wait()
        }

        const resource = this.free.shift()!
        const result = await callback(resource)

        this.add(resource)

        return result
    }

    add(resource: T) {
        this.free.push(resource)
        this.signals.signal()
    }
}
