self.addEventListener('install', () => {
    console.log("installing")
});
self.addEventListener('activate', () => {
});

// respond with a success
function successfulResponse(event, json){
    const errorFreeSerializer = () => {
        const seen = new WeakSet();
        return (key, value) => {
            if (typeof value === "object" && value !== null) {
                if (seen.has(value)) {
                    return;
                }
                seen.add(value);
            }
            return value;
        };
    };
    return new Response(JSON.stringify(json, errorFreeSerializer()), {
        status: 200
    })
}

const db = indexedDB.open("readandburn", 4);

const deepCopyHelper = (inObject, outObject, maxDepth=10) => {
    if (maxDepth === 0){
        return outObject
    }
    if (outObject === undefined) outObject = Array.isArray(inObject) ? [] : {}
    for (let key in inObject) {
        if (key === "__proto__") continue;
        let currObject = inObject[key]
        if (typeof currObject !== "object" || currObject === null) {
            outObject[key] = currObject;
        } else {
            outObject[key] = deepCopyHelper(currObject, outObject[key], maxDepth - 1)
        }
    }
    return outObject
}

const deepCopyDict = inObject => {
    let result = {};
    deepCopyHelper(inObject, result);
    return result;
}


const deepCopyArr = inObject => {
    let result = [];
    deepCopyHelper(inObject, result);
    return result;
}


db.onerror = function (event) {
    console.log('something wrong', event);
};

let cursor = null;
db.onsuccess = function (event) {
    cursor = db.result;
    console.log('db open', event);
};

db.onupgradeneeded = function (event) {
    console.log("upgrade")
    // create tables
    const cursor = event.target.result;
    if (!cursor.objectStoreNames.contains('messages')) {
        cursor.createObjectStore('messages', { autoIncrement: true });
    }
}

// get a key from indexeddb
function localStorageGetObjectify(key, callback){
    const objectStore = cursor.transaction(key).objectStore(key);
    let results = []
    objectStore.openCursor().onsuccess = function (event) {
        const result = event.target.result;
        if (result) {
            results.push(result.value);
            result.continue();
        } else {
            callback(results);
        }
    };
}

// set a key in indexeddb
function localStorageInsertObjectify(key, data){
    let request = cursor.transaction([key], "readwrite")
        .objectStore(key)
        .add(data);
    request.onsuccess = function (event) {
        console.log('success', event);
    };

    request.onerror = function (event) {
        console.log('failed', event);
    }
}

// clear local storage
function localStorageClear(key){
    let request = cursor.transaction([key], "readwrite")
        .objectStore(key)
        .clear();
    request.onsuccess = function (event) {
        console.log('success', event);
    };

    request.onerror = function (event) {
        console.log('failed', event);
    }
}

// regex for finding URL
const urlMather = /(?:(?:https?):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])/igm;

// convert message received from backend to be searchable
const messageMiddleware = (_v) => {
    return new Promise(resolve => {
        let v = deepCopyDict(_v);
        if (!v.links) v = {...v, links: {}, linkTexts: ""}
        let callbackCounters = 0
        try {
            let urls = v.message.match(urlMather);
            if (urls) urls.forEach((url) => {
                fetch(url).then(v => v.text()).then(respContent=> {
                    v.links[btoa(url)] = respContent;
                    v.linkTexts += respContent;
                    if (callbackCounters === url.length) resolve(v)
                }).catch(e => {console.log(e); resolve(v)})
            })
        } catch (e) { console.log(e) }
        return resolve(v)
    })
}

// convert all messages received from backend to be searchable
const messageMiddlewareAll = (_vs) => {
    return Promise.all(deepCopyArr(_vs).map(messageMiddleware))
}

// api prefix
const BASE = "/api"

self.addEventListener('fetch', async event => {
    const url = new URL(event.request.url);
    const method = event.request.method;

    if (url.origin === self.location.origin) {
        let splittedPath = url.pathname.split("/");
        switch (true) {
            // route for fetching all messages
            // first check with backend through api to see if there is any new message and store them to indexeddb if any
            // then open indexeddb to retrieve past messages
            case url.pathname.startsWith("/all_messages") && method === "GET":
                console.log("service worker proxying")
                return event.respondWith(new Promise(resolve => fetch(new Request(BASE + "/messages/" + splittedPath[splittedPath.length - 1], {
                    headers: {
                        ...(self.headers || {}),
                        ...event.request.headers,
                        "Who-The-Hell-Requested": "service-worker1",
                    },
                    method,
                }), {}).then(response => response.json()).then(response => {
                    if (!response.success)
                        return resolve(successfulResponse(event, response));
                    messageMiddlewareAll(response.messages).then(vs => {
                        vs.forEach(v => {
                            localStorageInsertObjectify("messages", v)
                        });
                        localStorageGetObjectify("messages", (v) => resolve(successfulResponse(event, {success: true, messages: v})));
                    })
                })));
            // route for sending message
            // first store the message into indexeddb then notify backend through api
            case url.pathname.startsWith("/send_messages") && method === "POST":
                console.log("service worker proxying")
                // eslint-disable-next-line no-case-declarations
                const userName = splittedPath[splittedPath.length - 1];
                return event.respondWith(new Promise(resolve => {
                    event.request.json().then(json => {
                        const content = json.message;
                        fetch(new Request(BASE + "/message/" + userName, {
                            headers: {
                                "Content-Type": "application/json",
                                ...(self.headers || {}),
                                ...event.request.headers,
                                "Who-The-Hell-Requested": "service-worker1",
                            },
                            method,
                            body: JSON.stringify(json)
                        }), {}).then(response => response.json()).then(response => {
                            if (!response.success)
                                return resolve(successfulResponse(event, response));
                            messageMiddleware({sender: userName + "@self", message: content}).then(v => {
                                localStorageInsertObjectify("messages", v)
                                localStorageGetObjectify("messages", (v) => resolve(successfulResponse(event, {
                                    success: true,
                                    messages: v
                                })))})})})}));
            // clear everything route
            // first clear everything in indexeddb then remove everything in backend
            case url.pathname.startsWith("/clear_all") && method === "GET":
                return event.respondWith(new Promise(resolve => fetch(new Request(BASE + "/message/clear", {
                    headers: {
                        ...(self.headers || {}),
                        ...event.request.headers,
                        "Who-The-Hell-Requested": "service-worker1",
                    },
                    method,
                }), {}).then(response => response.json()).then(() => {
                    localStorageClear("messages");
                    return resolve(successfulResponse(event, {success: true,}))
                })));
            // search route
            // find messages matching a keyword in indexeddb
            case url.pathname.startsWith("/search_all") && method === "GET":
                let query = url.search.split("find=")[1].split("&")[0];
                return event.respondWith(new Promise(resolve => {
                    return localStorageGetObjectify("messages", (messages) => {
                        let related_messages = [];
                        messages.forEach((v) => {
                            const {message, linkTexts} = v;
                            if ((message || "").includes(query) || (linkTexts || "").includes(query))
                                related_messages.push(v)
                        })
                        messageMiddlewareAll(related_messages).then(vs => {
                            resolve(successfulResponse(event, {success: true, related_messages: vs}))
                        })
                    })
                }));
            // other requests do no modification
            default:
                return event.respondWith(new Promise((resolve, reject) => {
                    fetch(new Request(event.request.url, {
                        headers: {
                            ...(self.headers || {}),
                            ...event.request.headers,
                            "Who-The-Hell-Requested": "service-worker2",
                        },
                        method,
                        body: event.request.body,
                    }), {}).then(resolve).catch(reject)
                }));
        }

    }

});