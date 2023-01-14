var re = /([^&=]+)=?([^&]*)/g;
var sanitize = function (str) {
    blacklist = ["__proto__", "constructor", "prototype"];
    blacklist.forEach((b) => {
        str = str.replace(b, b.toUpperCase());
    });
    return str
};
var decode = function (str) {
    return decodeURIComponent(str.replace(/\+/g, " "));
};
const parseParams = function (query) {
    // recursive function to construct the result object
    function createElement(params, key, value) {
        key = key + "";
        // if the key is a property
        if (key.indexOf(".") !== -1) {
            // extract the first part with the name of the object
            var list = key.split(".");
            // the rest of the key
            var new_key = key.split(/\.(.+)?/)[1];
            // create the object if it doesnt exist
            if (!params[list[0]]) params[list[0]] = {};
            // if the key is not empty, create it in the object
            if (new_key !== "") {
                createElement(params[list[0]], new_key, value);
            } else
                console.warn(
                    'parseParams :: empty property in key "' + key + '"'
                );
        }
        // if the key is an array
        else if (key.indexOf("[") !== -1) {
            // extract the array name
            var list = key.split("[");
            key = list[0];
            // extract the index of the array
            var list = list[1].split("]");
            var index = list[0];
            // if index is empty, just push the value at the end of the array
            if (index == "") {
                if (!params) params = {};
                if (!params[key] || !$.isArray(params[key])) params[key] = [];
                params[key].push(value);
            }
            // add the value at the index (must be an integer)
            else {
                if (!params) params = {};
                if (!params[key] || !$.isArray(params[key])) params[key] = [];
                params[key][parseInt(index)] = value;
            }
        }
        // just normal key
        else {
            if (!params) params = {};
            params[key] = value;
        }
    }
    // be sure the query is a string
    query = query + "";
    if (query === "") query = window.location + "";
    var params = {},
        e;
    if (query) {
        // remove # from end of query
        if (query.indexOf("#") !== -1) {
            query = query.substr(0, query.indexOf("#"));
        }

        // remove ? at the begining of the query
        if (query.indexOf("?") !== -1) {
            query = query.substr(query.indexOf("?") + 1, query.length);
        } else return {};
        // empty parameters
        if (query == "") return {};
        // execute a createElement on every key and value
        while ((e = re.exec(query))) {
            var key = decode(sanitize(e[1]));
            var value = decode(e[2]);
            createElement(params, key, value);
        }
    }
    return params;
};

(async () => {
    q = parseParams(location.href);
    if (!q.message) {
        const welcome = await (await fetch("/isLoggedIn", { credentials: "include" })).json();
        if (welcome.path) {
            window.location.href = welcome.path
        }else{
            alert(welcome.message)
        }
    } else {
        document.getElementById('name').innerText = `Welcome ${q.message.replace("Hello ", "")}`
    }
})();
