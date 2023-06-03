export function ref(target: any, propertyKey: string) {
    const idProp = propertyKey + '$id';
    const valProp = propertyKey + '$val';
    Object.defineProperty(target, propertyKey, {
        get() {
            if (!this[valProp] && this[idProp]) {
                const val = this.entity.world.getEntity(this[idProp]);
                if (!val)
                    throw new Error("Failed to resolve referenced entity: " + this[idProp]);
                Object.defineProperty(this, valProp, {value: val});
            }
            return this[valProp];
        },
        set(value) {
            this[idProp] = value.entity.id;
            Object.defineProperty(this, valProp, {value});
        }
    });
}
