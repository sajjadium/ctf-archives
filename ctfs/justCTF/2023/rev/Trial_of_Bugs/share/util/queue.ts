export class Queue<T> {
    private head: [any, T]|null = null;
    private tail: [any, T]|null = null;

    push(val: T) {
        if (this.tail) {
            this.tail[0] = [null, val];
            this.tail = this.tail[0];
        } else {
            this.head = this.tail = [null, val];
        }
    }

    peek(): T|null {
        return this.head ? this.head[1] : null;
    }

    pop(): T|null {
        if (!this.head)
            return null;
        const ret = this.head[1];
        this.head = this.head[0];
        if (!this.head)
            this.tail = null;
        return ret;
    }
}
