(async () => {
  const load = new Promise((resolve) => {
    window.addEventListener('load', resolve);
  });

  await load;

  // handle paste creation
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
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const { params } = parseForm(form);
    const { id } = await (
      await fetch('/api/pastes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      })
    ).json();
    window.location = `/paste/${id}`;
  });
})();
