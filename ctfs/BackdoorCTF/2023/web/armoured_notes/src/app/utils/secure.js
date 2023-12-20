const escapeHtmlReplaceMap = {
    '&': ';',
    "'": ';',
    '`': ';',
    '"': ';',
    '<': ';',
    '>': ';',
    "!":";",
    "_":";",
    "-":";",
    "*":";",
    "[":";",
    "{":";",
    "}":";",
    "|":";",
    "/":";",
    '"':";",
    '(':";",
    ')':";",
  }
  
  /**
   * @param {string} string
   * @returns {string}
   */
  export function escapeHtml(string) {
    return string.replace(/[&'`"<>]/g, (match) => escapeHtmlReplaceMap[match])
  }

  export function duplicate(body) {
    let obj={}
    let keys = Object.keys(body);
    keys.forEach((key) => {
      if(key !== "isAdmin")
      obj[key]=body[key];
    })
    return obj;
  }