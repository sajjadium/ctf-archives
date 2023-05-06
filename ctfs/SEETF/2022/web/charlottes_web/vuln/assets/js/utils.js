export const mapElement = (element, callback) => {
    for (let i = 0; i < element.children.length; i += 1) {
        mapElement(element.children[i], callback);
    }
    callback(element);
};

export const FONTS = [
    "Default",
    "Verdana",
    "Tahoma",
    "Georgia",
    "Andika",
    "Helvetica",
    "Arial",
    "Trebuuchet MS",
    "Times New Roman",
    "Courier New"
]

export const isObject = (obj) => {
    return typeof obj === 'function' || typeof obj === 'object';
}

export const merge = (target, source) => {
    for (let key in source) {
        if (isObject(target[key]) && isObject(source[key])) {
            merge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}

export const setStyle = (elem, propertyObject) => {
    for (var property in propertyObject)
        elem.style[property] = propertyObject[property];
}