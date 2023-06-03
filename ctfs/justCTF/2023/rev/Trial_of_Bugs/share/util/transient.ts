
export function transient(target: any, key: string, descriptor?: PropertyDescriptor) {
    if (!target.constructor.hasOwnProperty('transientProperties')) {
        target.constructor.transientProperties = [...(target.constructor.transientProperties || [])];
    }
    const props = target.constructor.transientProperties;
    props.push(key);
}

export function stripTransientProperties(obj: any, forceCopy: boolean = false) {
    if (!obj.constructor?.transientProperties)
        return forceCopy ? Object.assign({}, obj) : obj;
    const ret = Object.assign({}, obj);
    for (const prop of obj.constructor.transientProperties)
        delete ret[prop];
    return ret;
}
