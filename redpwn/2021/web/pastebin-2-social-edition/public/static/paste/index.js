(async () => {
  const load = new Promise((resolve) => {
    window.addEventListener('load', resolve);
  });

  // get id from URL
  const id = new URL(window.location).pathname.split('/')[2];

  // fetch paste contents
  const { content } = await (await fetch(`/api/pastes/${id}`)).json();

  // fetch paste comments
  const comments = await (await fetch(`/api/pastes/${id}/comments`)).json();

  await load;

  // populate paste area and comments
  const commentTemplate = document.querySelector('#comment-template');
  const commentContainer = document.querySelector('.comments');

  const addComment = (author, content) => {
    const current = commentTemplate.content.cloneNode(true);
    current.querySelector('.comment-author').textContent = `From ${author}:`;
    current.querySelector('.comment-content').textContent = content;
    commentContainer.appendChild(current);
  };

  for (const { author, content } of comments) addComment(author, content);

  document.querySelector('.paste').innerHTML = DOMPurify.sanitize(content);

  // handle comment submission
  const form = document.querySelector('form');

  // get form data into serializable object
  const parseForm = (form) => {
    const result = {};
    const fieldsets = form.querySelectorAll('fieldset');
    for (const fieldset of fieldsets) {
      const fieldsetName = decodeURIComponent(fieldset.name);
      if (!result[fieldsetName]) result[fieldsetName] = {};
      const inputs = fieldset.querySelectorAll('[name]');
      for (const input of inputs) {
        const inputName = decodeURIComponent(input.name);
        const inputValue = decodeURIComponent(input.value);
        result[fieldsetName][inputName] = inputValue;
      }
    }
    return result;
  };

  // add event listener for submission
  const errorContainer = document.querySelector('.error');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const { params } = parseForm(form);
    const { author, content, error, message } = await (
      await fetch(`/api/pastes/${id}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      })
    ).json();
    // if there's an error, show the message
    if (error) errorContainer.innerHTML = message;
    // otherwise, add the comment
    else {
      errorContainer.innerHTML = '';
      addComment(author, content);
    }
  });
})();
