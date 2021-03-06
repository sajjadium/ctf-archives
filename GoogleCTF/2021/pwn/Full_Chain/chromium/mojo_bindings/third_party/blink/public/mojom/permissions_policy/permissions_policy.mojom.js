// third_party/blink/public/mojom/permissions_policy/permissions_policy.mojom.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'third_party/blink/public/mojom/permissions_policy/permissions_policy.mojom';
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
  var origin$ =
      mojo.internal.exposeNamespace('url.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'url/mojom/origin.mojom', '../../../../../url/mojom/origin.mojom.js');
  }
  var permissions_policy_feature$ =
      mojo.internal.exposeNamespace('blink.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'third_party/blink/public/mojom/permissions_policy/permissions_policy_feature.mojom', 'permissions_policy_feature.mojom.js');
  }



  function ParsedPermissionsPolicyDeclaration(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  ParsedPermissionsPolicyDeclaration.prototype.initDefaults_ = function() {
    this.feature = 0;
    this.matchesAllOrigins = false;
    this.matchesOpaqueSrc = false;
    this.allowedOrigins = null;
  };
  ParsedPermissionsPolicyDeclaration.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  ParsedPermissionsPolicyDeclaration.validate = function(messageValidator, offset) {
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


    // validate ParsedPermissionsPolicyDeclaration.feature
    err = messageValidator.validateEnum(offset + codec.kStructHeaderSize + 0, permissions_policy_feature$.PermissionsPolicyFeature);
    if (err !== validator.validationError.NONE)
        return err;


    // validate ParsedPermissionsPolicyDeclaration.allowedOrigins
    err = messageValidator.validateArrayPointer(offset + codec.kStructHeaderSize + 8, 8, new codec.PointerTo(origin$.Origin), false, [0], 0);
    if (err !== validator.validationError.NONE)
        return err;



    return validator.validationError.NONE;
  };

  ParsedPermissionsPolicyDeclaration.encodedSize = codec.kStructHeaderSize + 16;

  ParsedPermissionsPolicyDeclaration.decode = function(decoder) {
    var packed;
    var val = new ParsedPermissionsPolicyDeclaration();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.feature =
        decoder.decodeStruct(new codec.Enum(permissions_policy_feature$.PermissionsPolicyFeature));
    packed = decoder.readUint8();
    val.matchesAllOrigins = (packed >> 0) & 1 ? true : false;
    val.matchesOpaqueSrc = (packed >> 1) & 1 ? true : false;
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    val.allowedOrigins =
        decoder.decodeArrayPointer(new codec.PointerTo(origin$.Origin));
    return val;
  };

  ParsedPermissionsPolicyDeclaration.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(ParsedPermissionsPolicyDeclaration.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.Int32, val.feature);
    packed = 0;
    packed |= (val.matchesAllOrigins & 1) << 0
    packed |= (val.matchesOpaqueSrc & 1) << 1
    encoder.writeUint8(packed);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.encodeArrayPointer(new codec.PointerTo(origin$.Origin), val.allowedOrigins);
  };
  exports.ParsedPermissionsPolicyDeclaration = ParsedPermissionsPolicyDeclaration;
})();