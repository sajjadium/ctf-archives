"use strict";
(function (){
  function isLocStringsScriptTag ( node ) {
    return node && 
      node.tagName === 'SCRIPT' &&
      node.type === 'application/json' &&
      node.classList.contains('localization_strings');
  }
  
  function parseJSONTextContent ( node ) {
    try {
      //this may failed if the content of the script tag is still not render.
      return JSON.parse(node.textContent);
    } catch ( error ) {
      return undefined;
    }
  }
  
  window.idms = window.idms || {};
  window.idms.app_config = window.idms.app_config || {};
  window.idms.app_config.i18n_legacy = window.idms.app_config.i18n_legacy || [];
  
  if (!window.idms.localizationStringsObserver) {
    var parsedJSONScripts = [];
    window.idms.localizationStringsObserver = new MutationObserver(function (mutationList) {
  
      var found = false;
  
      for (var i = 0; i < mutationList.length; i++) {
        var record = mutationList[i];
  
        for (var j = 0; j < record.addedNodes.length; j++) {
          var addedNode = record.addedNodes[j];
          var addedParentNode = addedNode.parentNode;
          var dataScriptNode = undefined;
          var newLocStrings = undefined;
  
          if(isLocStringsScriptTag(addedNode)) {
            dataScriptNode = addedNode;
          } else if (isLocStringsScriptTag(addedParentNode)) {
            dataScriptNode = addedParentNode;
          }
  
          if(dataScriptNode !== undefined && parsedJSONScripts.indexOf(dataScriptNode) < 0){
            newLocStrings = parseJSONTextContent(dataScriptNode);
            if(newLocStrings){
              parsedJSONScripts.push(dataScriptNode);
            }
          }
  
          if (!Array.isArray(newLocStrings)) {
            continue;
          }
  
          if (newLocStrings.length > 0) {
            found = true;
          }
          newLocStrings.forEach(function (locString) {
            window.idms.app_config.i18n_legacy.push(locString);
          });
        }
      }
  
      if (found && typeof window.idms.app_config.loadAppConfig === 'function') {
        window.idms.app_config.loadAppConfig({
          appConfig: {
            i18n_legacy: window.idms.app_config.i18n_legacy
          }
        });
      }
    });
  
  
    window.idms.localizationStringsObserver.observe(document.body, {subtree: true, childList: true});
  }
})()
