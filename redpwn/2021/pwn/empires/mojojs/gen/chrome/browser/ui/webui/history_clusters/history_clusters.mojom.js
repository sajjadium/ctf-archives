// chrome/browser/ui/webui/history_clusters/history_clusters.mojom.js is auto generated by mojom_bindings_generator.py, do not edit

// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

(function() {
  var mojomId = 'chrome/browser/ui/webui/history_clusters/history_clusters.mojom';
  if (mojo.internal.isMojomLoaded(mojomId)) {
    console.warn('The following mojom is loaded multiple times: ' + mojomId);
    return;
  }
  mojo.internal.markMojomLoaded(mojomId);
  var bindings = mojo;
  var associatedBindings = mojo;
  var codec = mojo.internal;
  var validator = mojo.internal;

  var exports = mojo.internal.exposeNamespace('historyClusters.mojom');
  var history_clusters$ =
      mojo.internal.exposeNamespace('historyClusters.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'components/history_clusters/core/history_clusters.mojom', '../../../../../components/history_clusters/core/history_clusters.mojom.js');
  }
  var url$ =
      mojo.internal.exposeNamespace('url.mojom');
  if (mojo.config.autoLoadMojomDeps) {
    mojo.internal.loadMojomIfNecessary(
        'url/mojom/url.mojom', '../../../../../url/mojom/url.mojom.js');
  }



  function QueryResult(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  QueryResult.prototype.initDefaults_ = function() {
    this.title = null;
    this.clusters = null;
    this.isContinuation = false;
    this.continuationQueryParams = null;
  };
  QueryResult.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  QueryResult.validate = function(messageValidator, offset) {
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


    // validate QueryResult.title
    err = messageValidator.validateStringPointer(offset + codec.kStructHeaderSize + 0, true)
    if (err !== validator.validationError.NONE)
        return err;


    // validate QueryResult.clusters
    err = messageValidator.validateArrayPointer(offset + codec.kStructHeaderSize + 8, 8, new codec.PointerTo(history_clusters$.Cluster), false, [0], 0);
    if (err !== validator.validationError.NONE)
        return err;



    // validate QueryResult.continuationQueryParams
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 24, history_clusters$.QueryParams, true);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  QueryResult.encodedSize = codec.kStructHeaderSize + 32;

  QueryResult.decode = function(decoder) {
    var packed;
    var val = new QueryResult();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.title =
        decoder.decodeStruct(codec.NullableString);
    val.clusters =
        decoder.decodeArrayPointer(new codec.PointerTo(history_clusters$.Cluster));
    packed = decoder.readUint8();
    val.isContinuation = (packed >> 0) & 1 ? true : false;
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    val.continuationQueryParams =
        decoder.decodeStructPointer(history_clusters$.QueryParams);
    return val;
  };

  QueryResult.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(QueryResult.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(codec.NullableString, val.title);
    encoder.encodeArrayPointer(new codec.PointerTo(history_clusters$.Cluster), val.clusters);
    packed = 0;
    packed |= (val.isContinuation & 1) << 0
    encoder.writeUint8(packed);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.encodeStructPointer(history_clusters$.QueryParams, val.continuationQueryParams);
  };
  function PageHandler_SetPage_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  PageHandler_SetPage_Params.prototype.initDefaults_ = function() {
    this.page = new PagePtr();
  };
  PageHandler_SetPage_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  PageHandler_SetPage_Params.validate = function(messageValidator, offset) {
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


    // validate PageHandler_SetPage_Params.page
    err = messageValidator.validateInterface(offset + codec.kStructHeaderSize + 0, false);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  PageHandler_SetPage_Params.encodedSize = codec.kStructHeaderSize + 8;

  PageHandler_SetPage_Params.decode = function(decoder) {
    var packed;
    var val = new PageHandler_SetPage_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.page =
        decoder.decodeStruct(new codec.Interface(PagePtr));
    return val;
  };

  PageHandler_SetPage_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(PageHandler_SetPage_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStruct(new codec.Interface(PagePtr), val.page);
  };
  function PageHandler_QueryClusters_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  PageHandler_QueryClusters_Params.prototype.initDefaults_ = function() {
    this.queryParams = null;
  };
  PageHandler_QueryClusters_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  PageHandler_QueryClusters_Params.validate = function(messageValidator, offset) {
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


    // validate PageHandler_QueryClusters_Params.queryParams
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, history_clusters$.QueryParams, false);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  PageHandler_QueryClusters_Params.encodedSize = codec.kStructHeaderSize + 8;

  PageHandler_QueryClusters_Params.decode = function(decoder) {
    var packed;
    var val = new PageHandler_QueryClusters_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.queryParams =
        decoder.decodeStructPointer(history_clusters$.QueryParams);
    return val;
  };

  PageHandler_QueryClusters_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(PageHandler_QueryClusters_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(history_clusters$.QueryParams, val.queryParams);
  };
  function PageHandler_RemoveVisits_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  PageHandler_RemoveVisits_Params.prototype.initDefaults_ = function() {
    this.visits = null;
  };
  PageHandler_RemoveVisits_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  PageHandler_RemoveVisits_Params.validate = function(messageValidator, offset) {
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


    // validate PageHandler_RemoveVisits_Params.visits
    err = messageValidator.validateArrayPointer(offset + codec.kStructHeaderSize + 0, 8, new codec.PointerTo(history_clusters$.URLVisit), false, [0], 0);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  PageHandler_RemoveVisits_Params.encodedSize = codec.kStructHeaderSize + 8;

  PageHandler_RemoveVisits_Params.decode = function(decoder) {
    var packed;
    var val = new PageHandler_RemoveVisits_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.visits =
        decoder.decodeArrayPointer(new codec.PointerTo(history_clusters$.URLVisit));
    return val;
  };

  PageHandler_RemoveVisits_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(PageHandler_RemoveVisits_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeArrayPointer(new codec.PointerTo(history_clusters$.URLVisit), val.visits);
  };
  function PageHandler_RemoveVisits_ResponseParams(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  PageHandler_RemoveVisits_ResponseParams.prototype.initDefaults_ = function() {
    this.accepted = false;
  };
  PageHandler_RemoveVisits_ResponseParams.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  PageHandler_RemoveVisits_ResponseParams.validate = function(messageValidator, offset) {
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


    return validator.validationError.NONE;
  };

  PageHandler_RemoveVisits_ResponseParams.encodedSize = codec.kStructHeaderSize + 8;

  PageHandler_RemoveVisits_ResponseParams.decode = function(decoder) {
    var packed;
    var val = new PageHandler_RemoveVisits_ResponseParams();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    packed = decoder.readUint8();
    val.accepted = (packed >> 0) & 1 ? true : false;
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    decoder.skip(1);
    return val;
  };

  PageHandler_RemoveVisits_ResponseParams.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(PageHandler_RemoveVisits_ResponseParams.encodedSize);
    encoder.writeUint32(0);
    packed = 0;
    packed |= (val.accepted & 1) << 0
    encoder.writeUint8(packed);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
    encoder.skip(1);
  };
  function Page_OnClustersQueryResult_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  Page_OnClustersQueryResult_Params.prototype.initDefaults_ = function() {
    this.result = null;
  };
  Page_OnClustersQueryResult_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  Page_OnClustersQueryResult_Params.validate = function(messageValidator, offset) {
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


    // validate Page_OnClustersQueryResult_Params.result
    err = messageValidator.validateStructPointer(offset + codec.kStructHeaderSize + 0, QueryResult, false);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  Page_OnClustersQueryResult_Params.encodedSize = codec.kStructHeaderSize + 8;

  Page_OnClustersQueryResult_Params.decode = function(decoder) {
    var packed;
    var val = new Page_OnClustersQueryResult_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.result =
        decoder.decodeStructPointer(QueryResult);
    return val;
  };

  Page_OnClustersQueryResult_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(Page_OnClustersQueryResult_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeStructPointer(QueryResult, val.result);
  };
  function Page_OnVisitsRemoved_Params(values) {
    this.initDefaults_();
    this.initFields_(values);
  }


  Page_OnVisitsRemoved_Params.prototype.initDefaults_ = function() {
    this.removedVisits = null;
  };
  Page_OnVisitsRemoved_Params.prototype.initFields_ = function(fields) {
    for(var field in fields) {
        if (this.hasOwnProperty(field))
          this[field] = fields[field];
    }
  };

  Page_OnVisitsRemoved_Params.validate = function(messageValidator, offset) {
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


    // validate Page_OnVisitsRemoved_Params.removedVisits
    err = messageValidator.validateArrayPointer(offset + codec.kStructHeaderSize + 0, 8, new codec.PointerTo(history_clusters$.URLVisit), false, [0], 0);
    if (err !== validator.validationError.NONE)
        return err;

    return validator.validationError.NONE;
  };

  Page_OnVisitsRemoved_Params.encodedSize = codec.kStructHeaderSize + 8;

  Page_OnVisitsRemoved_Params.decode = function(decoder) {
    var packed;
    var val = new Page_OnVisitsRemoved_Params();
    var numberOfBytes = decoder.readUint32();
    var version = decoder.readUint32();
    val.removedVisits =
        decoder.decodeArrayPointer(new codec.PointerTo(history_clusters$.URLVisit));
    return val;
  };

  Page_OnVisitsRemoved_Params.encode = function(encoder, val) {
    var packed;
    encoder.writeUint32(Page_OnVisitsRemoved_Params.encodedSize);
    encoder.writeUint32(0);
    encoder.encodeArrayPointer(new codec.PointerTo(history_clusters$.URLVisit), val.removedVisits);
  };
  var kPageHandler_SetPage_Name = 1808412540;
  var kPageHandler_QueryClusters_Name = 1695461483;
  var kPageHandler_RemoveVisits_Name = 472738274;

  function PageHandlerPtr(handleOrPtrInfo) {
    this.ptr = new bindings.InterfacePtrController(PageHandler,
                                                   handleOrPtrInfo);
  }

  function PageHandlerAssociatedPtr(associatedInterfacePtrInfo) {
    this.ptr = new associatedBindings.AssociatedInterfacePtrController(
        PageHandler, associatedInterfacePtrInfo);
  }

  PageHandlerAssociatedPtr.prototype =
      Object.create(PageHandlerPtr.prototype);
  PageHandlerAssociatedPtr.prototype.constructor =
      PageHandlerAssociatedPtr;

  function PageHandlerProxy(receiver) {
    this.receiver_ = receiver;
  }
  PageHandlerPtr.prototype.setPage = function() {
    return PageHandlerProxy.prototype.setPage
        .apply(this.ptr.getProxy(), arguments);
  };

  PageHandlerProxy.prototype.setPage = function(page) {
    var params_ = new PageHandler_SetPage_Params();
    params_.page = page;
    var builder = new codec.MessageV0Builder(
        kPageHandler_SetPage_Name,
        codec.align(PageHandler_SetPage_Params.encodedSize));
    builder.encodeStruct(PageHandler_SetPage_Params, params_);
    var message = builder.finish();
    this.receiver_.accept(message);
  };
  PageHandlerPtr.prototype.queryClusters = function() {
    return PageHandlerProxy.prototype.queryClusters
        .apply(this.ptr.getProxy(), arguments);
  };

  PageHandlerProxy.prototype.queryClusters = function(queryParams) {
    var params_ = new PageHandler_QueryClusters_Params();
    params_.queryParams = queryParams;
    var builder = new codec.MessageV0Builder(
        kPageHandler_QueryClusters_Name,
        codec.align(PageHandler_QueryClusters_Params.encodedSize));
    builder.encodeStruct(PageHandler_QueryClusters_Params, params_);
    var message = builder.finish();
    this.receiver_.accept(message);
  };
  PageHandlerPtr.prototype.removeVisits = function() {
    return PageHandlerProxy.prototype.removeVisits
        .apply(this.ptr.getProxy(), arguments);
  };

  PageHandlerProxy.prototype.removeVisits = function(visits) {
    var params_ = new PageHandler_RemoveVisits_Params();
    params_.visits = visits;
    return new Promise(function(resolve, reject) {
      var builder = new codec.MessageV1Builder(
          kPageHandler_RemoveVisits_Name,
          codec.align(PageHandler_RemoveVisits_Params.encodedSize),
          codec.kMessageExpectsResponse, 0);
      builder.encodeStruct(PageHandler_RemoveVisits_Params, params_);
      var message = builder.finish();
      this.receiver_.acceptAndExpectResponse(message).then(function(message) {
        var reader = new codec.MessageReader(message);
        var responseParams =
            reader.decodeStruct(PageHandler_RemoveVisits_ResponseParams);
        resolve(responseParams);
      }).catch(function(result) {
        reject(Error("Connection error: " + result));
      });
    }.bind(this));
  };

  function PageHandlerStub(delegate) {
    this.delegate_ = delegate;
  }
  PageHandlerStub.prototype.setPage = function(page) {
    return this.delegate_ && this.delegate_.setPage && this.delegate_.setPage(page);
  }
  PageHandlerStub.prototype.queryClusters = function(queryParams) {
    return this.delegate_ && this.delegate_.queryClusters && this.delegate_.queryClusters(queryParams);
  }
  PageHandlerStub.prototype.removeVisits = function(visits) {
    return this.delegate_ && this.delegate_.removeVisits && this.delegate_.removeVisits(visits);
  }

  PageHandlerStub.prototype.accept = function(message) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kPageHandler_SetPage_Name:
      var params = reader.decodeStruct(PageHandler_SetPage_Params);
      this.setPage(params.page);
      return true;
    case kPageHandler_QueryClusters_Name:
      var params = reader.decodeStruct(PageHandler_QueryClusters_Params);
      this.queryClusters(params.queryParams);
      return true;
    default:
      return false;
    }
  };

  PageHandlerStub.prototype.acceptWithResponder =
      function(message, responder) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kPageHandler_RemoveVisits_Name:
      var params = reader.decodeStruct(PageHandler_RemoveVisits_Params);
      this.removeVisits(params.visits).then(function(response) {
        var responseParams =
            new PageHandler_RemoveVisits_ResponseParams();
        responseParams.accepted = response.accepted;
        var builder = new codec.MessageV1Builder(
            kPageHandler_RemoveVisits_Name,
            codec.align(PageHandler_RemoveVisits_ResponseParams.encodedSize),
            codec.kMessageIsResponse, reader.requestID);
        builder.encodeStruct(PageHandler_RemoveVisits_ResponseParams,
                             responseParams);
        var message = builder.finish();
        responder.accept(message);
      });
      return true;
    default:
      return false;
    }
  };

  function validatePageHandlerRequest(messageValidator) {
    var message = messageValidator.message;
    var paramsClass = null;
    switch (message.getName()) {
      case kPageHandler_SetPage_Name:
        if (!message.expectsResponse() && !message.isResponse())
          paramsClass = PageHandler_SetPage_Params;
      break;
      case kPageHandler_QueryClusters_Name:
        if (!message.expectsResponse() && !message.isResponse())
          paramsClass = PageHandler_QueryClusters_Params;
      break;
      case kPageHandler_RemoveVisits_Name:
        if (message.expectsResponse())
          paramsClass = PageHandler_RemoveVisits_Params;
      break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  function validatePageHandlerResponse(messageValidator) {
   var message = messageValidator.message;
   var paramsClass = null;
   switch (message.getName()) {
      case kPageHandler_RemoveVisits_Name:
        if (message.isResponse())
          paramsClass = PageHandler_RemoveVisits_ResponseParams;
        break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  var PageHandler = {
    name: 'history_clusters.mojom.PageHandler',
    kVersion: 0,
    ptrClass: PageHandlerPtr,
    proxyClass: PageHandlerProxy,
    stubClass: PageHandlerStub,
    validateRequest: validatePageHandlerRequest,
    validateResponse: validatePageHandlerResponse,
  };
  PageHandlerStub.prototype.validator = validatePageHandlerRequest;
  PageHandlerProxy.prototype.validator = validatePageHandlerResponse;
  var kPage_OnClustersQueryResult_Name = 1788414703;
  var kPage_OnVisitsRemoved_Name = 1872536775;

  function PagePtr(handleOrPtrInfo) {
    this.ptr = new bindings.InterfacePtrController(Page,
                                                   handleOrPtrInfo);
  }

  function PageAssociatedPtr(associatedInterfacePtrInfo) {
    this.ptr = new associatedBindings.AssociatedInterfacePtrController(
        Page, associatedInterfacePtrInfo);
  }

  PageAssociatedPtr.prototype =
      Object.create(PagePtr.prototype);
  PageAssociatedPtr.prototype.constructor =
      PageAssociatedPtr;

  function PageProxy(receiver) {
    this.receiver_ = receiver;
  }
  PagePtr.prototype.onClustersQueryResult = function() {
    return PageProxy.prototype.onClustersQueryResult
        .apply(this.ptr.getProxy(), arguments);
  };

  PageProxy.prototype.onClustersQueryResult = function(result) {
    var params_ = new Page_OnClustersQueryResult_Params();
    params_.result = result;
    var builder = new codec.MessageV0Builder(
        kPage_OnClustersQueryResult_Name,
        codec.align(Page_OnClustersQueryResult_Params.encodedSize));
    builder.encodeStruct(Page_OnClustersQueryResult_Params, params_);
    var message = builder.finish();
    this.receiver_.accept(message);
  };
  PagePtr.prototype.onVisitsRemoved = function() {
    return PageProxy.prototype.onVisitsRemoved
        .apply(this.ptr.getProxy(), arguments);
  };

  PageProxy.prototype.onVisitsRemoved = function(removedVisits) {
    var params_ = new Page_OnVisitsRemoved_Params();
    params_.removedVisits = removedVisits;
    var builder = new codec.MessageV0Builder(
        kPage_OnVisitsRemoved_Name,
        codec.align(Page_OnVisitsRemoved_Params.encodedSize));
    builder.encodeStruct(Page_OnVisitsRemoved_Params, params_);
    var message = builder.finish();
    this.receiver_.accept(message);
  };

  function PageStub(delegate) {
    this.delegate_ = delegate;
  }
  PageStub.prototype.onClustersQueryResult = function(result) {
    return this.delegate_ && this.delegate_.onClustersQueryResult && this.delegate_.onClustersQueryResult(result);
  }
  PageStub.prototype.onVisitsRemoved = function(removedVisits) {
    return this.delegate_ && this.delegate_.onVisitsRemoved && this.delegate_.onVisitsRemoved(removedVisits);
  }

  PageStub.prototype.accept = function(message) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    case kPage_OnClustersQueryResult_Name:
      var params = reader.decodeStruct(Page_OnClustersQueryResult_Params);
      this.onClustersQueryResult(params.result);
      return true;
    case kPage_OnVisitsRemoved_Name:
      var params = reader.decodeStruct(Page_OnVisitsRemoved_Params);
      this.onVisitsRemoved(params.removedVisits);
      return true;
    default:
      return false;
    }
  };

  PageStub.prototype.acceptWithResponder =
      function(message, responder) {
    var reader = new codec.MessageReader(message);
    switch (reader.messageName) {
    default:
      return false;
    }
  };

  function validatePageRequest(messageValidator) {
    var message = messageValidator.message;
    var paramsClass = null;
    switch (message.getName()) {
      case kPage_OnClustersQueryResult_Name:
        if (!message.expectsResponse() && !message.isResponse())
          paramsClass = Page_OnClustersQueryResult_Params;
      break;
      case kPage_OnVisitsRemoved_Name:
        if (!message.expectsResponse() && !message.isResponse())
          paramsClass = Page_OnVisitsRemoved_Params;
      break;
    }
    if (paramsClass === null)
      return validator.validationError.NONE;
    return paramsClass.validate(messageValidator, messageValidator.message.getHeaderNumBytes());
  }

  function validatePageResponse(messageValidator) {
    return validator.validationError.NONE;
  }

  var Page = {
    name: 'history_clusters.mojom.Page',
    kVersion: 0,
    ptrClass: PagePtr,
    proxyClass: PageProxy,
    stubClass: PageStub,
    validateRequest: validatePageRequest,
    validateResponse: null,
  };
  PageStub.prototype.validator = validatePageRequest;
  PageProxy.prototype.validator = null;
  exports.QueryResult = QueryResult;
  exports.PageHandler = PageHandler;
  exports.PageHandlerPtr = PageHandlerPtr;
  exports.PageHandlerAssociatedPtr = PageHandlerAssociatedPtr;
  exports.Page = Page;
  exports.PagePtr = PagePtr;
  exports.PageAssociatedPtr = PageAssociatedPtr;
})();