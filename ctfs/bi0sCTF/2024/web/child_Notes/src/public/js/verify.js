async function check(rows, id) {
  var content = rows.filter((item) => item.id === id)[0];
  if (content) {
    return { delete: verify(content) };
  }
  return false;
}

async function all() {
  resp = await fetch(`/all`).then((resp) => resp.json());
  return resp;
}

async function del(id) {
  resp = await fetch(`/delete`, {
    method: "POST",
    body: "id=" + id,
  }).json();
  return resp.success;
}

async function init(rows) {
  rows = await all();
  posts = rows[0];
  users = rows[1];
  rows = posts.filter(
    (item) => item.id && item.title && item.content && item.author
  );
  rows = rows.map((item) => {
    item.author = users.filter((user) => user.username === item.author)[0];
    return item;
  });
}

async function verify(content) {
  // List of suspicious HTML patterns
  const maliciousPatterns = [
    /<script[\s>]/i,
    /<\/script[\s>]/i,
    /<iframe[\s>]/i,
    /<\/iframe[\s>]/i,
    /on\w+\s*=\s*"/i, // Matches any event handler like onclick, onmouseover, etc.
    /javascript:/i, // Matches 'javascript:' in attributes like href="javascript:..."
    /data:[^;]*;base64/i, // Matches data URI schemes, which can contain malicious code
  ];

  for (const pattern of maliciousPatterns) {
    if (pattern.test(content)) {
      return true; // Found a match, potentially malicious HTML
    }
  }
  return false; // No matches, input is likely safe
}
let rows;
init(rows);
