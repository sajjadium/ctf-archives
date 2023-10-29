const jws = require('jws')
const { KeyObject, createSecretKey, createPublicKey, createPrivateKey } = require("crypto");

const PUB_KEY_ALGS = ['RS256', 'RS384', 'RS512'];
const EC_KEY_ALGS = ['ES256', 'ES384', 'ES512'];
const RSA_KEY_ALGS = ['RS256', 'RS384', 'RS512'];
const HS_ALGS = ['HS256', 'HS384', 'HS512'];
const SUPPORTED_ALGS = ['RS256', 'RS384', 'RS512', 'ES256', 'ES384', 'ES512', 'HS256', 'HS384', 'HS512', 'none'];

const MAX_SAFE_INTEGER = 9007199254740991

var argsTag = '[object Arguments]',
    funcTag = '[object Function]',
    genTag = '[object GeneratorFunction]',
    stringTag = '[object String]',
    symbolTag = '[object Symbol]';

const allowedAlgorithmsForKeys = {
    'ec': ['ES256', 'ES384', 'ES512'],
    'rsa': ['RS256', 'PS256', 'RS384', 'PS384', 'RS512', 'PS512'],
    'rsa-pss': ['PS256', 'PS384', 'PS512']
};


function baseFindIndex(array, predicate, fromIndex, fromRight) {
    var length = array.length,
        index = fromIndex + (fromRight ? 1 : -1);

    while ((fromRight ? index-- : ++index < length)) {
        if (predicate(array[index], index, array)) {
            return index;
        }
    }
    return -1;
}

function baseIndexOf(array, value, fromIndex) {
    if (value !== value) {
        return baseFindIndex(array, baseIsNaN, fromIndex);
    }
    var index = fromIndex - 1,
        length = array.length;

    while (++index < length) {
        if (array[index] === value) {
            return index;
        }
    }
    return -1;
}
function isLength(value) {
    return typeof value == 'number' &&
        value > -1 && value % 1 == 0 && value <= MAX_SAFE_INTEGER;
}

function isObject(value) {
    var type = typeof value;
    return !!value && (type == 'object' || type == 'function');
}

function isFunction(value) {
    // The use of `Object#toString` avoids issues with the `typeof` operator

    var tag = isObject(value) ? Object.prototype.toString.call(value) : '';
    return tag == funcTag || tag == genTag;
}

function isArrayLike(value) {
    return value != null && isLength(value.length) && !isFunction(value);
}

function includes(collection, value, fromIndex, guard) {
    collection = isArrayLike(collection) ? collection : values(collection);
    fromIndex = (fromIndex && !guard) ? toInteger(fromIndex) : 0;

    var length = collection.length;
    if (fromIndex < 0) {
        fromIndex = nativeMax(length + fromIndex, 0);
    }
    return isString(collection)
        ? (fromIndex <= length && collection.indexOf(value, fromIndex) > -1)
        : (!!length && baseIndexOf(collection, value, fromIndex) > -1);
}

const sign_options_schema = {
    expiresIn: { isValid: function (value) { return isInteger(value) || (isString(value) && value); }, message: '"expiresIn" should be a number of seconds or string representing a timespan' },
    notBefore: { isValid: function (value) { return isInteger(value) || (isString(value) && value); }, message: '"notBefore" should be a number of seconds or string representing a timespan' },
    audience: { isValid: function (value) { return isString(value) || Array.isArray(value); }, message: '"audience" must be a string or array' },
    algorithm: { isValid: includes.bind(null, SUPPORTED_ALGS), message: '"algorithm" must be a valid string enum value' },
    header: { isValid: isPlainObject, message: '"header" must be an object' },
    encoding: { isValid: isString, message: '"encoding" must be a string' },
    issuer: { isValid: isString, message: '"issuer" must be a string' },
    subject: { isValid: isString, message: '"subject" must be a string' },
    jwtid: { isValid: isString, message: '"jwtid" must be a string' },
    noTimestamp: { isValid: isBoolean, message: '"noTimestamp" must be a boolean' },
    keyid: { isValid: isString, message: '"keyid" must be a string' },
    mutatePayload: { isValid: isBoolean, message: '"mutatePayload" must be a boolean' },
    allowInsecureKeySizes: { isValid: isBoolean, message: '"allowInsecureKeySizes" must be a boolean' },
    allowInvalidAsymmetricKeyTypes: { isValid: isBoolean, message: '"allowInvalidAsymmetricKeyTypes" must be a boolean' }
};

function isObjectLike(value) {
    return !!value && typeof value == 'object';
}

function isHostObject(value) {
    var result = false;
    if (value != null && typeof value.toString != 'function') {
        try {
            result = !!(value + '');
        } catch (e) { }
    }
    return result;
}

const isNumber = (value) => {
    return typeof value == 'number' ||
        (isObjectLike(value) && Object.prototype.toString.call(value) == '[object Number]');
}

function isString(value) {
    return typeof value == 'string' ||
        (!Array.isArray(value) && isObjectLike(value) && Object.prototype.toString.call(value) == '[object String]');
}

function isBoolean(value) {
    return value === true || value === false ||
        (isObjectLike(value) && Object.prototype.toString.call(value) == '[object Boolean]');
}

function isPlainObject(value) {
    if (!isObjectLike(value) ||
        Object.prototype.toString.call(value) != '[object Object]' || isHostObject(value)) {
        return false;
    }
    var proto = Object.getPrototypeOf(value);
    if (proto === null) {
        return true;
    }
    var Ctor = hasOwnProperty.call(proto, 'constructor') && proto.constructor;
    return (typeof Ctor == 'function' &&
        Ctor instanceof Ctor
        && Function.prototype.toString.call(Ctor) == Function.prototype.toString.call(Object));
}

const options_to_payload = {
    'audience': 'aud',
    'issuer': 'iss',
    'subject': 'sub',
    'jwtid': 'jti'
};

const registered_claims_schema = {
    iat: { isValid: isNumber, message: '"iat" should be a number of seconds' },
    exp: { isValid: isNumber, message: '"exp" should be a number of seconds' },
    nbf: { isValid: isNumber, message: '"nbf" should be a number of seconds' }
};

const JwtError = function (message, error) {
    Error.call(this, message);
    if (Error.captureStackTrace) {
        Error.captureStackTrace(this, this.constructor);
    }
    this.name = 'JsonWebTokenError';
    this.message = message;
    if (error) this.inner = error;
};

function validatePayload(payload) {
    return validate(registered_claims_schema, true, payload, 'payload');
}

function validateOptions(options) {
    return validate(sign_options_schema, false, options, 'options');
}


function validate(schema, allowUnknown, object, parameterName) {
    if (!isPlainObject(object)) {
        throw new Error('Expected "' + parameterName + '" to be a plain object.');
    }
    Object.keys(object)
        .forEach(function (key) {
            const validator = schema[key];
            if (!validator) {
                if (!allowUnknown) {
                    throw new Error('"' + key + '" is not allowed in "' + parameterName + '"');
                }
                return;
            }
            if (!validator.isValid(object[key])) {
                throw new Error(validator.message);
            }
        });
}

function validateAsymmetricKey(algorithm, key) {
    if (!algorithm || !key) return;

    const keyType = key.asymmetricKeyType;
    if (!keyType) return;

    const allowedAlgorithms = allowedAlgorithmsForKeys[keyType];

    if (!allowedAlgorithms) {
        throw new Error(`Unknown key type "${keyType}".`);
    }

    if (!allowedAlgorithms.includes(algorithm)) {
        throw new Error(`"alg" parameter for "${keyType}" key type must be one of: ${allowedAlgorithms.join(', ')}.`)
    }

    /* istanbul ignore next */
    switch (keyType) {
        case 'ec':
            const keyCurve = key.asymmetricKeyDetails.namedCurve;
            const allowedCurve = allowedCurves[algorithm];

            if (keyCurve !== allowedCurve) {
                throw new Error(`"alg" parameter "${algorithm}" requires curve "${allowedCurve}".`);
            }
            break;

        case 'rsa-pss':
            if (RSA_PSS_KEY_DETAILS_SUPPORTED) {
                const length = parseInt(algorithm.slice(-3), 10);
                const { hashAlgorithm, mgf1HashAlgorithm, saltLength } = key.asymmetricKeyDetails;

                if (hashAlgorithm !== `sha${length}` || mgf1HashAlgorithm !== hashAlgorithm) {
                    throw new Error(`Invalid key for this operation, its RSA-PSS parameters do not meet the requirements of "alg" ${algorithm}.`);
                }

                if (saltLength !== undefined && saltLength > length >> 3) {
                    throw new Error(`Invalid key for this operation, its RSA-PSS parameter saltLength does not meet the requirements of "alg" ${algorithm}.`)
                }
            }
            break;
    }
}


function decode(jwt, options) {
    options = options || {};
    var decoded = jws.decode(jwt, options);
    if (!decoded) { return null; }
    var payload = decoded.payload;

    //try parse the payload
    if (typeof payload === 'string') {
        try {
            var obj = JSON.parse(payload);
            if (obj !== null && typeof obj === 'object') {
                payload = obj;
            }
        } catch (e) { }
    }

    //return header if `complete` option is enabled.  header includes claims
    //such as `kid` and `alg` used to select the key within a JWKS needed to
    //verify the signature
    if (options.complete === true) {
        return {
            header: decoded.header,
            payload: payload,
            signature: decoded.signature
        };
    }
    return payload;
};

function sign(payload, key, options, callback) {
    if (typeof options === 'function') {
        callback = options;
        options = {};
    } else {
        options = options || {};
    }

    const isObjectPayload = typeof payload === 'object' && !Buffer.isBuffer(payload);

    const header = Object.assign({
        alg: options.algorithm || 'HS256',
        typ: isObjectPayload ? 'JWT' : undefined,
        kid: options.keyid
    }, options.header);

    const failure = (err) => {
        if (callback) {
            return callback(err);
        }
        throw err;
    }

    if (!key && options.algorithm !== 'none') {
        return failure(new Error('key must have a value'));
    }

    if (header.alg.startsWith('HS')) {
        key = createSecretKey(typeof key === 'string' ? Buffer.from(key) : key)
    } else if (/^(?:RS|PS|ES)/.test(header.alg)) {
        try{
            key = createPrivateKey(key)
        }catch(e){
            return failure(new Error('illegal asymmetric key???'));
        }
    } else {
        return failure(new Error('illegal key???'));
    }

    if (header.alg.startsWith('HS') && key.type !== 'secret') {
        return failure(new Error((`key must be a symmetric key when using ${header.alg}`)))
    } else if (/^(?:RS|PS|ES)/.test(header.alg)) {
        if (key.type !== 'private') {
            return failure(new Error((`key must be an asymmetric key when using ${header.alg}`)))
        }
        if (!options.allowInsecureKeySizes
            && !header.alg.startsWith('ES')
            && key.asymmetricKeyDetails !== undefined
            && key.asymmetricKeyDetails.modulusLength < 2048) {
            return failure(new Error(`key has a minimum key size of 2048 bits for ${header.alg}`));
        }
    }

    if (typeof payload === 'undefined') {
        return failure(new Error('payload is required'));
    } else if (isObjectPayload) {
        try {
            validatePayload(payload);
        }
        catch (error) {
            return failure(error);
        }
        if (!options.mutatePayload) {
            payload = Object.assign({}, payload);
        }
    } else {
        const invalid_options = options_for_objects.filter(function (opt) {
            return typeof options[opt] !== 'undefined';
        });

        if (invalid_options.length > 0) {
            return failure(new Error('invalid ' + invalid_options.join(',') + ' option for ' + (typeof payload) + ' payload'));
        }
    }

    if (typeof payload.exp !== 'undefined' && typeof options.expiresIn !== 'undefined') {
        return failure(new Error('Bad "options.expiresIn" option the payload already has an "exp" property.'));
    }

    if (typeof payload.nbf !== 'undefined' && typeof options.notBefore !== 'undefined') {
        return failure(new Error('Bad "options.notBefore" option the payload already has an "nbf" property.'));
    }

    try {
        validateOptions(options);
    }
    catch (error) {
        return failure(error);
    }

    if (!options.allowInvalidAsymmetricKeyTypes) {
        try {
            validateAsymmetricKey(header.alg, key);
        } catch (error) {
            return failure(error);
        }
    }

    const timestamp = payload.iat || Math.floor(Date.now() / 1000);

    if (options.noTimestamp) {
        delete payload.iat;
    } else if (isObjectPayload) {
        payload.iat = timestamp;
    }

    if (typeof options.notBefore !== 'undefined') {
        try {
            payload.nbf = timespan(options.notBefore, timestamp);
        }
        catch (err) {
            return failure(err);
        }
        if (typeof payload.nbf === 'undefined') {
            return failure(new Error('"notBefore" should be a number of seconds or string representing a timespan eg: "1d", "20h", 60'));
        }
    }

    if (typeof options.expiresIn !== 'undefined' && typeof payload === 'object') {
        try {
            payload.exp = timespan(options.expiresIn, timestamp);
        }
        catch (err) {
            return failure(err);
        }
        if (typeof payload.exp === 'undefined') {
            return failure(new Error('"expiresIn" should be a number of seconds or string representing a timespan eg: "1d", "20h", 60'));
        }
    }

    Object.keys(options_to_payload).forEach(function (key) {
        const claim = options_to_payload[key];
        if (typeof options[key] !== 'undefined') {
            if (typeof payload[claim] !== 'undefined') {
                return failure(new Error('Bad "options.' + key + '" option. The payload already has an "' + claim + '" property.'));
            }
            payload[claim] = options[key];
        }
    });

    const encoding = options.encoding || 'utf8';

    if (typeof callback === 'function') {
        callback = callback && once(callback);

        jws.createSign({
            header: header,
            privateKey: key,
            payload: payload,
            encoding: encoding
        }).once('error', callback)
            .once('done', function (signature) {
                if (!options.allowInsecureKeySizes && /^(?:RS|PS)/.test(header.alg) && signature.length < 256) {
                    return callback(new Error(`key has a minimum key size of 2048 bits for ${header.alg}`))
                }
                callback(null, signature);
            });
    } else {
        let signature = jws.sign({ header: header, payload: payload, secret: key, encoding: encoding });
        if (!options.allowInsecureKeySizes && /^(?:RS|PS)/.test(header.alg) && signature.length < 256) {
            throw new Error(`key has a minimum key size of 2048 bits for ${header.alg}`)
        }
        return signature
    }
};


function verify(jwtString, key, options, callback) {
    if ((typeof options === 'function') && !callback) {
        callback = options;
        options = {};
    }

    if (!options) {
        options = {};
    }

    options = Object.assign({}, options);

    let done;

    if (callback) {
        done = callback;
    } else {
        done = function (err, data) {
            if (err) throw err;
            return data;
        };
    }

    if (options.clockTimestamp && typeof options.clockTimestamp !== 'number') {
        return done(new JwtError('clockTimestamp must be a number'));
    }

    if (options.nonce !== undefined && (typeof options.nonce !== 'string' || options.nonce.trim() === '')) {
        return done(new JwtError('nonce must be a non-empty string'));
    }

    if (options.allowInvalidAsymmetricKeyTypes !== undefined && typeof options.allowInvalidAsymmetricKeyTypes !== 'boolean') {
        return done(new JwtError('allowInvalidAsymmetricKeyTypes must be a boolean'));
    }

    const clockTimestamp = options.clockTimestamp || Math.floor(Date.now() / 1000);

    if (!jwtString) {
        return done(new JwtError('jwt must be provided'));
    }

    if (typeof jwtString !== 'string') {
        return done(new JwtError('jwt must be a string'));
    }

    const parts = jwtString.split('.');

    if (parts.length !== 3) {
        return done(new JwtError('jwt malformed'));
    }

    let decodedToken;

    try {
        decodedToken = decode(jwtString, { complete: true });
    } catch (err) {
        return done(err);
    }

    if (!decodedToken) {
        return done(new JwtError('invalid token'));
    }

    const header = decodedToken.header;
    let getSecret;

    if (typeof key === 'function') {
        if (!callback) {
            return done(new JwtError('verify must be called asynchronous if secret or public key is provided as a callback'));
        }

        getSecret = key;
    }
    else {
        getSecret = (header, secretCallback) => {
            return secretCallback(null, key);
        };
    }

    return getSecret(header, (err, key) => {
        if (err) {
            return done(new JwtError('error in secret or public key callback: ' + err.message));
        }

        const hasSignature = parts[2].trim() !== '';

        if (!hasSignature && key) {
            return done(new JwtError('jwt signature is required'));
        }

        if (hasSignature && !key) {
            return done(new JwtError('secret or public key must be provided'));
        }

        if (!hasSignature && !options.algorithms) {
            return done(new JwtError('please specify "none" in "algorithms" to verify unsigned tokens'));
        }

        if (header.alg.startsWith('HS')) {
            key = createSecretKey(typeof key === 'string' ? Buffer.from(key) : key)
        } else if (/^(?:RS|PS|ES)/.test(header.alg)) {
            try{
                key = createPublicKey(key)
            }catch(e){
                return failure(new Error('illegal asymmetric key???'));
            }
        } else {
            return failure(new Error('illegal key???'));
        }

        if (!options.algorithms) {
            if (key.type === 'secret') {
                options.algorithms = HS_ALGS;
            } else if (['rsa', 'rsa-pss'].includes(key.asymmetricKeyType)) {
                options.algorithms = RSA_KEY_ALGS
            } else if (key.asymmetricKeyType === 'ec') {
                options.algorithms = EC_KEY_ALGS
            } else {
                options.algorithms = PUB_KEY_ALGS
            }
        }

        if (options.algorithms.indexOf(decodedToken.header.alg) === -1) {
            return done(new JwtError('invalid algorithm'));
        }

        if (header.alg.startsWith('HS') && key.type !== 'secret') {
            return done(new JwtError((`secretOrPublicKey must be a symmetric key when using ${header.alg}`)))
        } else if (/^(?:RS|PS|ES)/.test(header.alg) && key.type !== 'public') {
            return done(new JwtError((`secretOrPublicKey must be an asymmetric key when using ${header.alg}`)))
        }

        if (!options.allowInvalidAsymmetricKeyTypes) {
            try {
                validateAsymmetricKey(header.alg, key);
            } catch (e) {
                return done(e);
            }
        }

        let valid;

        try {
            valid = jws.verify(jwtString, decodedToken.header.alg, key);
        } catch (e) {
            return done(e);
        }

        if (!valid) {
            return done(new JwtError('invalid signature'));
        }

        const payload = decodedToken.payload;

        if (typeof payload.nbf !== 'undefined' && !options.ignoreNotBefore) {
            if (typeof payload.nbf !== 'number') {
                return done(new JwtError('invalid nbf value'));
            }
            if (payload.nbf > clockTimestamp + (options.clockTolerance || 0)) {
                return done(new NotBeforeError('jwt not active', new Date(payload.nbf * 1000)));
            }
        }

        if (typeof payload.exp !== 'undefined' && !options.ignoreExpiration) {
            if (typeof payload.exp !== 'number') {
                return done(new JwtError('invalid exp value'));
            }
            if (clockTimestamp >= payload.exp + (options.clockTolerance || 0)) {
                return done(new TokenExpiredError('jwt expired', new Date(payload.exp * 1000)));
            }
        }

        if (options.audience) {
            const audiences = Array.isArray(options.audience) ? options.audience : [options.audience];
            const target = Array.isArray(payload.aud) ? payload.aud : [payload.aud];

            const match = target.some(function (targetAudience) {
                return audiences.some(function (audience) {
                    return audience instanceof RegExp ? audience.test(targetAudience) : audience === targetAudience;
                });
            });

            if (!match) {
                return done(new JwtError('jwt audience invalid. expected: ' + audiences.join(' or ')));
            }
        }

        if (options.issuer) {
            const invalid_issuer =
                (typeof options.issuer === 'string' && payload.iss !== options.issuer) ||
                (Array.isArray(options.issuer) && options.issuer.indexOf(payload.iss) === -1);

            if (invalid_issuer) {
                return done(new JwtError('jwt issuer invalid. expected: ' + options.issuer));
            }
        }

        if (options.subject) {
            if (payload.sub !== options.subject) {
                return done(new JwtError('jwt subject invalid. expected: ' + options.subject));
            }
        }

        if (options.jwtid) {
            if (payload.jti !== options.jwtid) {
                return done(new JwtError('jwt jwtid invalid. expected: ' + options.jwtid));
            }
        }

        if (options.nonce) {
            if (payload.nonce !== options.nonce) {
                return done(new JwtError('jwt nonce invalid. expected: ' + options.nonce));
            }
        }

        if (options.maxAge) {
            if (typeof payload.iat !== 'number') {
                return done(new JwtError('iat required when maxAge is specified'));
            }

            const maxAgeTimestamp = timespan(options.maxAge, payload.iat);
            if (typeof maxAgeTimestamp === 'undefined') {
                return done(new JwtError('"maxAge" should be a number of seconds or string representing a timespan eg: "1d", "20h", 60'));
            }
            if (clockTimestamp >= maxAgeTimestamp + (options.clockTolerance || 0)) {
                return done(new TokenExpiredError('maxAge exceeded', new Date(maxAgeTimestamp * 1000)));
            }
        }

        if (options.complete === true) {
            const signature = decodedToken.signature;

            return done(null, {
                header: header,
                payload: payload,
                signature: signature
            });
        }

        return done(null, payload);
    });
};

function decode(jwt, options) {
    options = options || {};
    var decoded = jws.decode(jwt, options);
    if (!decoded) { return null; }
    var payload = decoded.payload;

    if (typeof payload === 'string') {
        try {
            var obj = JSON.parse(payload);
            if (obj !== null && typeof obj === 'object') {
                payload = obj;
            }
        } catch (e) { }
    }

    if (options.complete === true) {
        return {
            header: decoded.header,
            payload: payload,
            signature: decoded.signature
        };
    }
    return payload;
};


module.exports.verify = verify
module.exports.sign = sign
module.exports.decode = decode