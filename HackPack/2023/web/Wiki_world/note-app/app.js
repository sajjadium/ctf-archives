(function() {
    function renderNote() {
        const note = atob( window.location.hash.slice(1) );
        const santizedNote = DOMPurify.sanitize(note, {ALLOWED_URI_REGEXP: /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|cid|xmpp|whatsapp|skype|teamspeak|webcal|slack|ms\-teams|zoommtg|facetime|gtalk|feed|svn|git|ssh|sftp|data|blob|filesystem):|$)/i});
        document.querySelector( '#display' ).innerHTML = santizedNote;
    }

    addEventListener( 'hashchange', renderNote);
    
    renderNote();

    addEventListener( 'load', function() {
        document.querySelector( '#note-button' ).addEventListener( 'click', function(event) {
            event.preventDefault();
            const note = document.querySelector( '#note-input' ).value;
            window.location.hash = btoa( note );
         });
    } )
})();
