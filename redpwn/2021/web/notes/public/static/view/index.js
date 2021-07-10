const template = document.querySelector('#note-template').innerHTML;
const container = document.querySelector('.container');
const user = new URL(window.location).pathname.split('/')[2];

const populateTemplate = (template, params) =>
  template.replace(/\{\{\s?(.+?)\s?\}\}/g, (match, param) => params[param]);

(async () => {
  const request = await fetch(`/api/notes/${user}`);
  const notes = await request.json();

  const renderedNotes = [];
  for (const note of notes) {
    // this one is controlled by user, so prevent xss
    const body = note.body
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll('\'', '&#39;');
    // this one isn't, but make sure it fits on page
    const tag =
      note.tag.length > 10 ? note.tag.substring(0, 7) + '...' : note.tag;
    // render templates and put them in our array
    const rendered = populateTemplate(template, { body, tag });
    renderedNotes.push(rendered);
  }

  container.innerHTML += renderedNotes.join('');
})();
