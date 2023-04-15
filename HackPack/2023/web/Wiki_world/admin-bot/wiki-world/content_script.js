addEventListener( 'load', function() {
  document.querySelectorAll( 'input' ).forEach( elem => {
    elem.addEventListener( 'change', show );
  } );
  document.querySelectorAll( 'textarea' ).forEach( elem => {
    elem.addEventListener( 'change', show );
  });

  async function show( event ) {
    var config = window.config || {};
    config.WIKI_REGEX = config.WIKI_REGEX || '\\[INSERT WIKI-EXCERPT BLOB:([a-zA-Z0-9_|!=+\\-]+)\\]';
    config.WIKIPEDIA_SERVER = config.WIKIPEDIA_SERVER || 'https://en.wikipedia.org/w/api.php';
    const data = event.target.value;
    const matches = new RegExp( config.WIKI_REGEX, 'gmi' ).exec( data );
    if ( matches ) {
      const resp = await fetch(`${config.WIKIPEDIA_SERVER}`, { method: 'POST', body: new URLSearchParams({
        "origin": "*",
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": matches[1],
        "formatversion": "2",
        "exsentences": "10",
        "exlimit": "1",
        "explaintext": 1
      }) } );

      const json = await resp.json();
      event.target.value = data.replace( matches[0], json.query.pages[0].extract );
    }
  }
});
