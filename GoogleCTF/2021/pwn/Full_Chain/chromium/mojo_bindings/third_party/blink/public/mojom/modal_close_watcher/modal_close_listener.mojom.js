// third_party/blink/public/mojom/modal_close_watcher/modal_close_listener.mojom.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'third_party/blink/public/mojom/modal_close_watcher/modal_close_listener.mojom';
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



  function ModalCloseListener_Signal_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  ModalCloseListener_Signal_Params.prototype.initDefaults_ = function() {
  };
  ModalCloseListener_Signal_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  ModalCloseListener_Signal_Params.validate = function(messageValidator, offset) {
    var err;
    err = messageValidator.validateStructHeader(offset, codec.kStructHeaderSize);
    if (err !== validator.validationError.NONE)
        return err;

    var kVersionSizes = [
      {version: 0, numBytes: 8}
    ];
    err = messageValidator.validateStructVersion(offset, kVersionSizes);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  ModalCloseListener_Signal_Params.encodedSize = codec.kStructHeaderSize + 0;

  ModalCloseListener_Signal_Params.decode = function(decoder) {
    var packed;
    var val = new ModalCloseListener_Signal_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    return val;
  };

  ModalCloseListener_Signal_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(ModalCloseListener_Signal_Params.encodedSize);
    encoder.writeUint32(0);
  };
  var kModalCloseListener_Signal_Name = 0;

  function ModalCloseListenerPtr(handleOrPtrInfo) {
    this.ptr = new bindings.InterfacePtrController(ModalCloseListener,
                                                   handleOrPtrInfo);
  }

  function ModalCloseListenerAssociatedPtr(associatedInterfacePtrInfo) {
    this.ptr = new associatedBindings.AssociatedInterfacePtrController(
        ModalCloseListener, associatedInterfacePtrInfo);
  }

  ModalCloseListenerAssociatedPtr.prototype =
      Object.create(ModalCloseListenerPtr.prototype);
  ModalCloseListenerAssociatedPtr.prototype.constructor =
      ModalCloseListenerAssociatedPtr;

  function ModalCloseListenerProxy(receiver) {
    this.receiver_ = receiver;
  }
  ModalCloseListenerPtr.prototype.signal = function() {
    return ModalCloseListenerProxy.prototype.signal
        .apply(this.ptr.getProxy(), arguments);
  };

  ModalCloseListenerProxy.prototype.signal = function() {
    var params_ = new ModalCloseListener_Signal_Params();
    var builder = new codec.MessageV0Builder(
        kModalCloseListener_Signal_Name,
        codec.align(ModalCloseListener_Signal_Params.encodedSize));
    builder.encodeStruct(ModalCloseListener_Signal_Params, params_);
    var message = builder.finish();
    this.receiver_.accept(message);
  };

  function ModalCloseListenerStub(delegate) {
    this.delegate_ = delegate;
  }
  ModalCloseListenerStub.prototype.signal = function() {
    return this.delegate_ && this.delegate_.signal && this.delegate_.signal();
  }

  ModalCloseListenerStub.prototype.accept = function(message) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kModalCloseListener_Signal_Name:
      var params = reader.decodeStruct(ModalCloseListener_Signal_Params);
      this.signal();
      return true;
    default:
      return false;
    }
  };

  ModalCloseListenerStub.prototype.acceptWithResponder =
      function(message, responder) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    default:
      return false;
    }
  };

  function validateModalCloseListenerRequest(messageValidator) {
    var message = messageValidator.message;
    var paramsClass = null;
    switch (message.getName()) {
      case kModalCloseListener_Signal_Name:
        if (!message.expectsResponse() && !message.isResponse())
          paramsClass = ModalCloseListener_Signal_Params;
      break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  function validateModalCloseListenerResponse(messageValidator) {
    return validator.validationError.NONE;
  }

  var ModalCloseListener = {
    name: 'blink.mojom.ModalCloseListener',
    kVersion: 0,
    ptrClass: ModalCloseListenerPtr,
    proxyClass: ModalCloseListenerProxy,
    stubClass: ModalCloseListenerStub,
    validateRequest: validateModalCloseListenerRequest,
    validateResponse: null,
  };
  ModalCloseListenerStub.prototype.validator = validateModalCloseListenerRequest;
  ModalCloseListenerProxy.prototype.validator = null;
  exports.ModalCloseListener = ModalCloseListener;
  exports.ModalCloseListenerPtr = ModalCloseListenerPtr;
  exports.ModalCloseListenerAssociatedPtr = ModalCloseListenerAssociatedPtr;
})();