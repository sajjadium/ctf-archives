// services/network/public/mojom/early_hints.mojom.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'services/network/public/mojom/early_hints.mojom';
  if (mojo.internal.isMojomLoaded(mojomId)) {
    console.warn('The following mojom is loaded multiple times: ' + mojomId);
    return;
  }
  mojo.internal.markMojomLoaded(mojomId);
  var bindings = mojo;
  var associatedBindings = mojo;
  var codec = mojo.internal;
  var validator = mojo.internal;

  var exports = mojo.internal.exposeNamespace('network.mojom');
  var parsed_headers$ =
      mojo.internal.exposeNamespace('network.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'services/network/public/mojom/parsed_headers.mojom', 'parsed_headers.mojom.js');
  }



  function EarlyHints(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  EarlyHints.prototype.initDefaults_ = function() {
    this.headers = null;
  };
  EarlyHints.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  EarlyHints.validate = function(messageValidator, offset) {
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


    // validate EarlyHints.headers
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, parsed_headers$.ParsedHeaders, false);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  EarlyHints.encodedSize = codec.kStructHeaderSize + 8;

  EarlyHints.decode = function(decoder) {
    var packed;
    var val = new EarlyHints();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.headers =
        decoder.decodeStructPointer(parsed_headers$.ParsedHeaders);
    return val;
  };

  EarlyHints.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(EarlyHints.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(parsed_headers$.ParsedHeaders, val.headers);
  };
  exports.EarlyHints = EarlyHints;
})();