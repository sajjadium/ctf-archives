// third_party/blink/public/mojom/desert.mojom.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'third_party/blink/public/mojom/desert.mojom';
  if (mojo.internal.isMojomLoaded(mojomId)) {
    console.warn('The following mojom is loaded multiple times: ' + mojomId);
    return;
  }
  mojo.internal.markMojomLoaded(mojomId);
  var bindings = mojo;
  var associatedBindings = mojo;
  var codec = mojo.internal;
  var validator = mojo.internal;

  var exports = mojo.internal.exposeNamespace('blink.mojom');
  var big_buffer$ =
      mojo.internal.exposeNamespace('mojoBase.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'mojo/public/mojom/base/big_buffer.mojom', '../../../../mojo/public/mojom/base/big_buffer.mojom.js');
  }
  var unguessable_token$ =
      mojo.internal.exposeNamespace('mojoBase.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'mojo/public/mojom/base/unguessable_token.mojom', '../../../../mojo/public/mojom/base/unguessable_token.mojom.js');
  }


  var DesertType = {};
  DesertType.DESOLATE = 4919;
  DesertType.EMPTY = 29489;
  DesertType.MIN_VALUE = 4919;
  DesertType.MAX_VALUE = 29489;

  DesertType.isKnownEnumValue = function(value) {
    switch (value) {
    case 4919:
    case 29489:
      return true;
    }
    return false;
  };

  DesertType.toKnownEnumValue = function(value) {
    return value;
  };

  DesertType.validate = function(enumValue) {
    const isExtensible = false;
    if (isExtensible || this.isKnownEnumValue(enumValue))
      return validator.validationError.NONE;

    return validator.validationError.UNKNOWN_ENUM_VALUE;
  };

  function Wreck(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  Wreck.prototype.initDefaults_ = function() {
    this.size = 0;
    this.lengthToUse = 0;
    this.data = null;
    this.type = 0;
  };
  Wreck.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  Wreck.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 40}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;




    // validate Wreck.data
    err = messageValidator.validateUnion(offset + codec.kStructHeaderSize + 8, big_buffer$.BigBuffer, true);
    if (err !== validator.validationError.NONE)
        return err;


    // validate Wreck.type
    err = messageValidator.validateEnum(offset + codec.kStructHeaderSize + 24, DesertType);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  Wreck.encodedSize = codec.kStructHeaderSize + 32;

  Wreck.decode = function(decoder) {
    var packed;
    var val = new Wreck();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.size =
        decoder.decodeStruct(codec.Uint32);
    val.lengthToUse =
        decoder.decodeStruct(codec.Uint32);
    val.data =
        decoder.decodeStruct(big_buffer$.BigBuffer);
    val.type =
        decoder.decodeStruct(new codec.Enum(DesertType));
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    return val;
  };

  Wreck.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(Wreck.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Uint32, val.size);
    encoder.encodeStruct(codec.Uint32, val.lengthToUse);
    encoder.encodeStruct(big_buffer$.BigBuffer, val.data);
    encoder.encodeStruct(codec.Int32, val.type);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
  };
  function Sand(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  Sand.prototype.initDefaults_ = function() {
    this.wrecks = null;
  };
  Sand.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  Sand.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 16}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate Sand.wrecks
    err = messageValidator.validateArrayPointer(offset + codec.kStructHeaderSize + 0, 8, new codec.PointerTo(Wreck), false, [0], 0);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  Sand.encodedSize = codec.kStructHeaderSize + 8;

  Sand.decode = function(decoder) {
    var packed;
    var val = new Sand();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.wrecks =
        decoder.decodeArrayPointer(new codec.PointerTo(Wreck));
    return val;
  };

  Sand.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(Sand.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeArrayPointer(new codec.PointerTo(Wreck), val.wrecks);
  };
  function Ozymandias_Visage_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  Ozymandias_Visage_Params.prototype.initDefaults_ = function() {
    this.command = null;
    this.secret = null;
  };
  Ozymandias_Visage_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  Ozymandias_Visage_Params.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 24}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate Ozymandias_Visage_Params.command
    err = messageValidator.validateArrayPointer(offset + codec.kStructHeaderSize + 0, 1, codec.Uint8, false, [0], 0);
    if (err !== validator.validationError.NONE)
        return err;


    // validate Ozymandias_Visage_Params.secret
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 8, unguessable_token$.UnguessableToken, false);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  Ozymandias_Visage_Params.encodedSize = codec.kStructHeaderSize + 16;

  Ozymandias_Visage_Params.decode = function(decoder) {
    var packed;
    var val = new Ozymandias_Visage_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.command =
        decoder.decodeArrayPointer(codec.Uint8);
    val.secret =
        decoder.decodeStructPointer(unguessable_token$.UnguessableToken);
    return val;
  };

  Ozymandias_Visage_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(Ozymandias_Visage_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeArrayPointer(codec.Uint8, val.command);
    encoder.encodeStructPointer(unguessable_token$.UnguessableToken, val.secret);
  };
  function Ozymandias_Despair_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  Ozymandias_Despair_Params.prototype.initDefaults_ = function() {
    this.sand = null;
  };
  Ozymandias_Despair_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  Ozymandias_Despair_Params.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 16}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate Ozymandias_Despair_Params.sand
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, Sand, false);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  Ozymandias_Despair_Params.encodedSize = codec.kStructHeaderSize + 8;

  Ozymandias_Despair_Params.decode = function(decoder) {
    var packed;
    var val = new Ozymandias_Despair_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.sand =
        decoder.decodeStructPointer(Sand);
    return val;
  };

  Ozymandias_Despair_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(Ozymandias_Despair_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(Sand, val.sand);
  };
  function Ozymandias_Despair_ResponseParams(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  Ozymandias_Despair_ResponseParams.prototype.initDefaults_ = function() {
    this.decay = null;
  };
  Ozymandias_Despair_ResponseParams.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  Ozymandias_Despair_ResponseParams.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 16}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;


    // validate Ozymandias_Despair_ResponseParams.decay
    err = messageValidator.validateArrayPointer(offset + codec.kStructHeaderSize + 0, 16, big_buffer$.BigBuffer, false, [0], 0);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  Ozymandias_Despair_ResponseParams.encodedSize = codec.kStructHeaderSize + 8;

  Ozymandias_Despair_ResponseParams.decode = function(decoder) {
    var packed;
    var val = new Ozymandias_Despair_ResponseParams();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.decay =
        decoder.decodeArrayPointer(big_buffer$.BigBuffer);
    return val;
  };

  Ozymandias_Despair_ResponseParams.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(Ozymandias_Despair_ResponseParams.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeArrayPointer(big_buffer$.BigBuffer, val.decay);
  };
  var kOzymandias_Visage_Name = 0;
  var kOzymandias_Despair_Name = 1;

  function OzymandiasPtr(handleOrPtrInfo) {
    this.ptr = new bindings.InterfacePtrController(Ozymandias,
                                                   handleOrPtrInfo);
  }

  function OzymandiasAssociatedPtr(associatedInterfacePtrInfo) {
    this.ptr = new associatedBindings.AssociatedInterfacePtrController(
        Ozymandias, associatedInterfacePtrInfo);
  }

  OzymandiasAssociatedPtr.prototype =
      Object.create(OzymandiasPtr.prototype);
  OzymandiasAssociatedPtr.prototype.constructor =
      OzymandiasAssociatedPtr;

  function OzymandiasProxy(receiver) {
    this.receiver_ = receiver;
  }
  OzymandiasPtr.prototype.visage = function() {
    return OzymandiasProxy.prototype.visage
        .apply(this.ptr.getProxy(), arguments);
  };

  OzymandiasProxy.prototype.visage = function(command, secret) {
    var params_ = new Ozymandias_Visage_Params();
    params_.command = command;
    params_.secret = secret;
    var builder = new codec.MessageV0Builder(
        kOzymandias_Visage_Name,
        codec.align(Ozymandias_Visage_Params.encodedSize));
    builder.encodeStruct(Ozymandias_Visage_Params, params_);
    var message = builder.finish();
    this.receiver_.accept(message);
  };
  OzymandiasPtr.prototype.despair = function() {
    return OzymandiasProxy.prototype.despair
        .apply(this.ptr.getProxy(), arguments);
  };

  OzymandiasProxy.prototype.despair = function(sand) {
    var params_ = new Ozymandias_Despair_Params();
    params_.sand = sand;
    return new Promise(function(resolve, reject) {
      var builder = new codec.MessageV1Builder(
          kOzymandias_Despair_Name,
          codec.align(Ozymandias_Despair_Params.encodedSize),
          codec.kMessageExpectsResponse, 0);
      builder.encodeStruct(Ozymandias_Despair_Params, params_);
      var message = builder.finish();
      this.receiver_.acceptAndExpectResponse(message).then(function(message) {
        var reader = new codec.MessageReader(message);
        var responseParams =
            reader.decodeStruct(Ozymandias_Despair_ResponseParams);
        resolve(responseParams);
      }).catch(function(result) {
        reject(Error("Connection error: " + result));
      });
    }.bind(this));
  };

  function OzymandiasStub(delegate) {
    this.delegate_ = delegate;
  }
  OzymandiasStub.prototype.visage = function(command, secret) {
    return this.delegate_ && this.delegate_.visage && this.delegate_.visage(command, secret);
  }
  OzymandiasStub.prototype.despair = function(sand) {
    return this.delegate_ && this.delegate_.despair && this.delegate_.despair(sand);
  }

  OzymandiasStub.prototype.accept = function(message) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kOzymandias_Visage_Name:
      var params = reader.decodeStruct(Ozymandias_Visage_Params);
      this.visage(params.command, params.secret);
      return true;
    default:
      return false;
    }
  };

  OzymandiasStub.prototype.acceptWithResponder =
      function(message, responder) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kOzymandias_Despair_Name:
      var params = reader.decodeStruct(Ozymandias_Despair_Params);
      this.despair(params.sand).then(function(response) {
        var responseParams =
            new Ozymandias_Despair_ResponseParams();
        responseParams.decay = response.decay;
        var builder = new codec.MessageV1Builder(
            kOzymandias_Despair_Name,
            codec.align(Ozymandias_Despair_ResponseParams.encodedSize),
            codec.kMessageIsResponse, reader.requestID);
        builder.encodeStruct(Ozymandias_Despair_ResponseParams,
                             responseParams);
        var message = builder.finish();
        responder.accept(message);
      });
      return true;
    default:
      return false;
    }
  };

  function validateOzymandiasRequest(messageValidator) {
    var message = messageValidator.message;
    var paramsClass = null;
    switch (message.getName()) {
      case kOzymandias_Visage_Name:
        if (!message.expectsResponse() && !message.isResponse())
          paramsClass = Ozymandias_Visage_Params;
      break;
      case kOzymandias_Despair_Name:
        if (message.expectsResponse())
          paramsClass = Ozymandias_Despair_Params;
      break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  function validateOzymandiasResponse(messageValidator) {
   var message = messageValidator.message;
   var paramsClass = null;
   switch (message.getName()) {
      case kOzymandias_Despair_Name:
        if (message.isResponse())
          paramsClass = Ozymandias_Despair_ResponseParams;
        break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  var Ozymandias = {
    name: 'blink.mojom.Ozymandias',
    kVersion: 0,
    ptrClass: OzymandiasPtr,
    proxyClass: OzymandiasProxy,
    stubClass: OzymandiasStub,
    validateRequest: validateOzymandiasRequest,
    validateResponse: validateOzymandiasResponse,
  };
  OzymandiasStub.prototype.validator = validateOzymandiasRequest;
  OzymandiasProxy.prototype.validator = validateOzymandiasResponse;
  exports.DesertType = DesertType;
  exports.Wreck = Wreck;
  exports.Sand = Sand;
  exports.Ozymandias = Ozymandias;
  exports.OzymandiasPtr = OzymandiasPtr;
  exports.OzymandiasAssociatedPtr = OzymandiasAssociatedPtr;
})();