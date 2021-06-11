const DEFAULT_OPTIONS = {
  allowedTags: [ 'B', 'I', 'EM', 'STRONG', 'DIV', 'P', 'SPAN', 'IMG' ]
};

// TODO: Writing our own sanitizer is probably fine, right?
function sanitize(input, options) {
  const template = document.createElement("template");
  template.innerHTML = input;
  const content = template.content;

  Array.from(content.querySelectorAll("*")).forEach((element) => {
    const allowedTags = options.allowedTags || [];
    if (!allowedTags.includes(element.tagName)) {
      element.remove();
    } else {
      const allowedAttrs = options.allowedAttrs || [];
      const attrs = Array.from(element.attributes);
      attrs.forEach(
        (attr) => {
          if (!allowedAttrs.includes(attr.name)) {
            element.removeAttributeNode(attr);
          }
        }
      );
    }
  });

  return template.innerHTML;
}

window.onload = () => {

  const params = new URLSearchParams(document.location.search);
  const id = params.get('id');

  // Initialize app state and request message and current user
  const state = {};
  Promise.all([
    fetch(`/message/${id}`)
      .then(r => r.json())
      .then(msg => {
        state.message = msg;
      }),
    fetch("/user")
      .then(r => r.json())
      .then(user => {
        state.user = user;
      })
  ]).then((r) => {

    // Allow devs to augment the state in the browser for debug purposes
    // TODO: Should we be leaving this in production builds?
    let debugParam = params.get("debug");
    if (debugParam) {
      let debug = JSON.parse(debugParam);

      for (const [key, value] of Object.entries(debug)) {
        state[key] = Object.assign(state[key], value);
      }
    }

    // Sanitize and insert content into page
    if (state.message !== null) {
      message.innerHTML = sanitize(state.message.message, DEFAULT_OPTIONS);
      from.innerHTML = `Message from ${sanitize(state.message.email, DEFAULT_OPTIONS)}`
    } else {
      from.innerHTML = state.user ? "Invalid message id" : "Login to view messages";
    }
    if (state.user !== null) {
      user.innerHTML = sanitize(state.user.name, DEFAULT_OPTIONS);
    }
  }).catch((e) => {
    console.log(e);
  });
}
    