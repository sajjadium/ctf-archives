// third_party/blink/public/mojom/webid/federated_auth_request.mojom.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'third_party/blink/public/mojom/webid/federated_auth_request.mojom';
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
  var url$ =
      mojo.internal.exposeNamespace('url.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'url/mojom/url.mojom', '../../../../../url/mojom/url.mojom.js');
  }


  var RequestIdTokenStatus = {};
  RequestIdTokenStatus.kSuccess = 0;
  RequestIdTokenStatus.kApprovalDeclined = 1;
  RequestIdTokenStatus.kErrorTooManyRequests = 2;
  RequestIdTokenStatus.kErrorWebIdNotSupportedByProvider = 3;
  RequestIdTokenStatus.kErrorFetchingWellKnown = 4;
  RequestIdTokenStatus.kErrorInvalidWellKnown = 5;
  RequestIdTokenStatus.kErrorFetchingSignin = 6;
  RequestIdTokenStatus.kErrorInvalidSigninResponse = 7;
  RequestIdTokenStatus.kError = 8;
  RequestIdTokenStatus.MIN_VALUE = 0,
  RequestIdTokenStatus.MAX_VALUE = 8,

  RequestIdTokenStatus.isKnownEnumValue = function(value) {
    switch (value) {
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 8:
      return true;
    }
    return false;
  };

  RequestIdTokenStatus.validate = function(enumValue) {
    var isExtensible = false;
    if (isExtensible || this.isKnownEnumValue(enumValue))
      return validator.validationError.NONE;

    return validator.validationError.UNKNOWN_ENUM_VALUE;
  };

  function FederatedAuthRequest_RequestIdToken_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  FederatedAuthRequest_RequestIdToken_Params.prototype.initDefaults_ = function() {
    this.provider = null;
    this.idRequest = null;
  };
  FederatedAuthRequest_RequestIdToken_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  FederatedAuthRequest_RequestIdToken_Params.validate = function(messageValidator, offset) {
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


    // validate FederatedAuthRequest_RequestIdToken_Params.provider
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, url$.Url, false);
    if (err !== validator.validationError.NONE)
        return err;


    // validate FederatedAuthRequest_RequestIdToken_Params.idRequest
    err = messageValidator.validateStringPointer(offset + codec.kStructHeaderSize + 8, false)
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  FederatedAuthRequest_RequestIdToken_Params.encodedSize = codec.kStructHeaderSize + 16;

  FederatedAuthRequest_RequestIdToken_Params.decode = function(decoder) {
    var packed;
    var val = new FederatedAuthRequest_RequestIdToken_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.provider =
        decoder.decodeStructPointer(url$.Url);
    val.idRequest =
        decoder.decodeStruct(codec.String);
    return val;
  };

  FederatedAuthRequest_RequestIdToken_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(FederatedAuthRequest_RequestIdToken_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(url$.Url, val.provider);
    encoder.encodeStruct(codec.String, val.idRequest);
  };
  function FederatedAuthRequest_RequestIdToken_ResponseParams(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  FederatedAuthRequest_RequestIdToken_ResponseParams.prototype.initDefaults_ = function() {
    this.status = 0;
    this.idToken = null;
  };
  FederatedAuthRequest_RequestIdToken_ResponseParams.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  FederatedAuthRequest_RequestIdToken_ResponseParams.validate = function(messageValidator, offset) {
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


    // validate FederatedAuthRequest_RequestIdToken_ResponseParams.status
    err = messageValidator.validateEnum(offset + codec.kStructHeaderSize + 0, RequestIdTokenStatus);
    if (err !== validator.validationError.NONE)
        return err;


    // validate FederatedAuthRequest_RequestIdToken_ResponseParams.idToken
    err = messageValidator.validateStringPointer(offset + codec.kStructHeaderSize + 8, true)
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  FederatedAuthRequest_RequestIdToken_ResponseParams.encodedSize = codec.kStructHeaderSize + 16;

  FederatedAuthRequest_RequestIdToken_ResponseParams.decode = function(decoder) {
    var packed;
    var val = new FederatedAuthRequest_RequestIdToken_ResponseParams();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.status =
        decoder.decodeStruct(codec.Int32);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    val.idToken =
        decoder.decodeStruct(codec.NullableString);
    return val;
  };

  FederatedAuthRequest_RequestIdToken_ResponseParams.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(FederatedAuthRequest_RequestIdToken_ResponseParams.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Int32, val.status);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.encodeStruct(codec.NullableString, val.idToken);
  };
  var kFederatedAuthRequest_RequestIdToken_Name = 0;

  function FederatedAuthRequestPtr(handleOrPtrInfo) {
    this.ptr = new bindings.InterfacePtrController(FederatedAuthRequest,
                                                   handleOrPtrInfo);
  }

  function FederatedAuthRequestAssociatedPtr(associatedInterfacePtrInfo) {
    this.ptr = new associatedBindings.AssociatedInterfacePtrController(
        FederatedAuthRequest, associatedInterfacePtrInfo);
  }

  FederatedAuthRequestAssociatedPtr.prototype =
      Object.create(FederatedAuthRequestPtr.prototype);
  FederatedAuthRequestAssociatedPtr.prototype.constructor =
      FederatedAuthRequestAssociatedPtr;

  function FederatedAuthRequestProxy(receiver) {
    this.receiver_ = receiver;
  }
  FederatedAuthRequestPtr.prototype.requestIdToken = function() {
    return FederatedAuthRequestProxy.prototype.requestIdToken
        .apply(this.ptr.getProxy(), arguments);
  };

  FederatedAuthRequestProxy.prototype.requestIdToken = function(provider, idRequest) {
    var params_ = new FederatedAuthRequest_RequestIdToken_Params();
    params_.provider = provider;
    params_.idRequest = idRequest;
    return new Promise(function(resolve, reject) {
      var builder = new codec.MessageV1Builder(
          kFederatedAuthRequest_RequestIdToken_Name,
          codec.align(FederatedAuthRequest_RequestIdToken_Params.encodedSize),
          codec.kMessageExpectsResponse, 0);
      builder.encodeStruct(FederatedAuthRequest_RequestIdToken_Params, params_);
      var message = builder.finish();
      this.receiver_.acceptAndExpectResponse(message).then(function(message) {
        var reader = new codec.MessageReader(message);
        var responseParams =
            reader.decodeStruct(FederatedAuthRequest_RequestIdToken_ResponseParams);
        resolve(responseParams);
      }).catch(function(result) {
        reject(Error("Connection error: " + result));
      });
    }.bind(this));
  };

  function FederatedAuthRequestStub(delegate) {
    this.delegate_ = delegate;
  }
  FederatedAuthRequestStub.prototype.requestIdToken = function(provider, idRequest) {
    return this.delegate_ && this.delegate_.requestIdToken && this.delegate_.requestIdToken(provider, idRequest);
  }

  FederatedAuthRequestStub.prototype.accept = function(message) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    default:
      return false;
    }
  };

  FederatedAuthRequestStub.prototype.acceptWithResponder =
      function(message, responder) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kFederatedAuthRequest_RequestIdToken_Name:
      var params = reader.decodeStruct(FederatedAuthRequest_RequestIdToken_Params);
      this.requestIdToken(params.provider, params.idRequest).then(function(response) {
        var responseParams =
            new FederatedAuthRequest_RequestIdToken_ResponseParams();
        responseParams.status = response.status;
        responseParams.idToken = response.idToken;
        var builder = new codec.MessageV1Builder(
            kFederatedAuthRequest_RequestIdToken_Name,
            codec.align(FederatedAuthRequest_RequestIdToken_ResponseParams.encodedSize),
            codec.kMessageIsResponse, reader.requestID);
        builder.encodeStruct(FederatedAuthRequest_RequestIdToken_ResponseParams,
                             responseParams);
        var message = builder.finish();
        responder.accept(message);
      });
      return true;
    default:
      return false;
    }
  };

  function validateFederatedAuthRequestRequest(messageValidator) {
    var message = messageValidator.message;
    var paramsClass = null;
    switch (message.getName()) {
      case kFederatedAuthRequest_RequestIdToken_Name:
        if (message.expectsResponse())
          paramsClass = FederatedAuthRequest_RequestIdToken_Params;
      break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  function validateFederatedAuthRequestResponse(messageValidator) {
   var message = messageValidator.message;
   var paramsClass = null;
   switch (message.getName()) {
      case kFederatedAuthRequest_RequestIdToken_Name:
        if (message.isResponse())
          paramsClass = FederatedAuthRequest_RequestIdToken_ResponseParams;
        break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  var FederatedAuthRequest = {
    name: 'blink.mojom.FederatedAuthRequest',
    kVersion: 0,
    ptrClass: FederatedAuthRequestPtr,
    proxyClass: FederatedAuthRequestProxy,
    stubClass: FederatedAuthRequestStub,
    validateRequest: validateFederatedAuthRequestRequest,
    validateResponse: validateFederatedAuthRequestResponse,
  };
  FederatedAuthRequestStub.prototype.validator = validateFederatedAuthRequestRequest;
  FederatedAuthRequestProxy.prototype.validator = validateFederatedAuthRequestResponse;
  exports.RequestIdTokenStatus = RequestIdTokenStatus;
  exports.FederatedAuthRequest = FederatedAuthRequest;
  exports.FederatedAuthRequestPtr = FederatedAuthRequestPtr;
  exports.FederatedAuthRequestAssociatedPtr = FederatedAuthRequestAssociatedPtr;
})();