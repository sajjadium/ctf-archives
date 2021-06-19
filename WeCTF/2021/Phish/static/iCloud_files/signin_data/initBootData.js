"use strict";
(function (){

  /*
    bootArgs has the structure:

    bootArgs.additional = {} full of known arguments with specific js that must be applied,
      ex: functions, string values that need to be manipulated prior to being set, etc
    bootArgs.direct = {} keys/values which can be set wholesale into bootData.
  */

  function populateFromBootArgs(bootArgs) {
    window.idms = window.idms || {};
    window.idms.app_config = window.idms.app_config || {};
    window.idms.app_config.bootData = window.idms.app_config.bootData || {};
    var bootData = window.idms.app_config.bootData;


  // Process all direct fields into place
    if (typeof bootArgs.direct === 'object') {
      Object.keys(bootArgs.direct).forEach(function (key) {
        bootData[key] = bootArgs.direct[key];
      });
    }

  // Functions for setting the the additional variables from the bootArgs
    /**
     * Function to get the value at bootArgs.additional[pathElements], iterating through the elements
     * @param pathElements a JS array of nested object names
     * @returns the value at bootArgs.additional[pathElements] or undefined if none exists.
     */
    function getBootArgsVal(pathElements) {
      if (typeof bootArgs.additional !== 'object') {
        return undefined;
      }

      var bootArgsVal = bootArgs.additional;

      for (var i in pathElements) {
        var pathElement = pathElements[i];
        if (typeof bootArgsVal[pathElement] !== "undefined") {
          bootArgsVal = bootArgsVal[pathElement];
        } else {
          bootArgsVal = undefined;
          break;
        }
      }
      return bootArgsVal;
    }

    /**
     * Sets the value on bootData of the specified path to the specified value, creating objects in the path if they are not defined
     * @param pathElements a JS array fo nested object names
     * @param valueToSet the value to set to the path
     */
    function setBootDataValue(pathElements, valueToSet) {
      var bootDataVal = bootData;
      var pathElementsExceptLast = pathElements.slice(0, -1);

      var valid = true;
      for (var i in pathElementsExceptLast) {
        var pathElement = pathElementsExceptLast[i];
        // if the next bootDataVal is not defined, then make it an object.
        if (typeof bootDataVal[pathElement] === 'undefined') {
          bootDataVal[pathElement] = {};
        }
        if (typeof bootDataVal[pathElement] === 'object') {
          bootDataVal = bootDataVal[pathElement];
        } else {
          valid = false;
          break;
        }
      }

      var lastPathElement = pathElements[pathElements.length - 1];
      if (valid) {
        bootDataVal[lastPathElement] = valueToSet;
      }
    }

    /**
     * Function which checks for eligability of a path, then runs a function if present to modify the value
     * @param pathToModify The path to check
     * @param modificationFunc A function which takes 1 argument (from bootArgs) and returns a value to be set in bootData,
     *                         if not provided, just passes the value through.
     */
    function useIfExists(pathToModify, modificationFunc) {
      if (typeof pathToModify !== 'string' || !pathToModify) {
        return;
      }
      var pathElements = pathToModify.split(/\./);

      // needs to be some path
      if (pathElements.length === 0) {
        return;
      }

      var bootArgsVal = getBootArgsVal(pathElements);
      if (!bootArgsVal) {
        // bootArgs.additional does not have the specified path, so just return.
        return;
      }

      // If it's not a function then set up a no-op function
      if (typeof modificationFunc !== 'function') {
        modificationFunc = function (val) {
          return val;
        };
      }

      var valueToSet = modificationFunc(bootArgsVal);
      if (typeof valueToSet !== 'undefined') {
        setBootDataValue(pathElements, valueToSet);
      }
    }

    // Begin block of changes that are passed in

    useIfExists("isCacheData", function (val) {
      // if this is present, we want to overwrite the destinationDomain and redirect URI
      // with the existing cached widget domain
      bootData.destinationDomain = window.idms.widgetDomain;
      if (bootData.appleOAuth && bootData.appleOAuth.requestor) {
        bootData.appleOAuth.requestor.redirectURI = window.idms.widgetDomain;
      }
      return undefined;
    });

    useIfExists("skVersion", function(val) {
      if (val === '7') {
        window.idms.app_config.idmswcConfig = {
          formStyle: 'sasskit7'
        };
      }
      return undefined;
    });

    useIfExists("canRoute2sv", function(val) {
      window.idms.app_config.loadAppConfig({
        appConfig: {
          bootData: bootData
        }
      });
      can.route.attr('route', '2sv');
      return undefined;
    });

    useIfExists("formStyle", function(val) {
      window.idms.app_config.idmswcConfig = {
        formStyle: val
      };
      return undefined;
    });

    useIfExists("origin", function(val) {
      return window.location.origin;
    });

    // End block of changes that are passed in

  }

  function isBootArgsScriptTag ( node ) {
    return node && 
      node.tagName === 'SCRIPT' &&
      node.type === 'application/json' &&
      node.classList.contains('boot_args');
  }

  function parseJSONTextContent ( node ) {
    try {
      //this may failed if the content of the script tag is still not render.
      return JSON.parse(node.textContent);
    } catch ( error ) {
      return undefined;
    }
  }

  if (!(window.idms && window.idms.bootArgsObserver)) {
    var parsedJSONScripts = [];
    window.idms = window.idms || {};
    window.idms.bootArgsObserver = new MutationObserver(function (mutationList) {

      for (var i = 0; i < mutationList.length; i++) {
        var record = mutationList[i];

        for (var j = 0; j < record.addedNodes.length; j++) {

          var addedNode = record.addedNodes[j];
          var addedParentNode = addedNode.parentNode;
          var bootArgsScriptNode = undefined;

          if(isBootArgsScriptTag(addedNode)) {
            bootArgsScriptNode = addedNode;
          } else if (isBootArgsScriptTag(addedParentNode)) {
            bootArgsScriptNode = addedParentNode;
          }

          if(bootArgsScriptNode && parsedJSONScripts.indexOf(bootArgsScriptNode) < 0){
            var data = parseJSONTextContent(bootArgsScriptNode);
            if(data) {
              parsedJSONScripts.push(bootArgsScriptNode);
              populateFromBootArgs(data);
            }
          }       
        }
      }
    });

    window.idms.bootArgsObserver.observe(document.body, {subtree: true, childList: true});
  }
})();
