window.onload = async function(){
    //init
    document.body.highlighted_note = await get_higlighted_note();
    document.body.search_result = document.getElementById('search_result');
    document.body.search_content = document.getElementById('search_content')
    document.body.search_open = document.getElementById('search_open')

    //highlight note
    document.getElementById('highlighted').innerHTML = document.body.highlighted_note;

    //search handler
    document.getElementById('search_button').onclick = search_click;
}

async function search_click(){
    search_name({'query':document.body.search_content.value, 'open' : document.body.search_open.checked})
}

window.addEventListener('hashchange', async function(){
    let search_query = JSON.parse(atob(location.hash.substring(1)));
    search_name(search_query);
});

async function search_name(search_data){
    let should_open = search_data['open']
    let query = search_data['query']

    let notes = await get_all_notes();

    let found_note = notes.find((val) => val.note.toString().startsWith(query));
    if(found_note == undefined){
        document.body.search_result.href = '';
        document.body.search_result.text = 'NOT FOUND'
        document.body.search_result.innerHTML += '<br>'
    }

    document.body.search_result.href = `note/${found_note.name}`;
    document.body.search_result.text = 'FOUND'
    document.body.search_result.innerHTML += '<br>'
    if(should_open)document.body.search_result.click();
}

async function get_all_notes(){
    return await Promise.all((await (await fetch('/notes')).json()).map(async (name) => ({'name':name, 'note': (await get_note(name))})))
}

async function get_higlighted_note(){
    return get_note((await (await fetch('/highlighted_note')).text()));
}

async function get_note(name){
    return (await (await fetch(`/note/${name}`)).text());
}

