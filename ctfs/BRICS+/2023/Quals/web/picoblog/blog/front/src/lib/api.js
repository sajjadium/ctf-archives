/**
 * @param {string} method
 * @param {string} url
 * @param {string?} body
 * @param {boolean} sameorigin
 * @param {boolean} cachebust
 * @returns {Promise<Response>}
 */
async function request(method, url, body, sameorigin, cachebust) {
  /** @type {RequestInit} */
  const params = {
    method,
    mode: "cors",
    credentials: "omit",
  };

  if (sameorigin) {
    params.mode = "same-origin";
    params.credentials = "same-origin";
  }

  if (body) {
    params.headers = params.headers || {};
    params.headers = {
      "content-type": "application/json",
    };
    params.body = body;
  }

  if (cachebust) {
    params.headers = params.headers || {};
    params.headers = {
      pragma: "no-cache",
    };
  }

  return fetch(url, params);
}

/**
 * @param {string} url
 * @param {Object} body
 * @param {boolean} sameorigin
 * @returns {Promise<Response>}
 */
async function post(url, body, sameorigin) {
  return request("POST", url, JSON.stringify(body), sameorigin, false);
}

/**
 * @param {string} url
 * @param {boolean} sameorigin
 * @param {boolean} cachebust
 * @returns {Promise<Response>}
 */
async function get(url, sameorigin, cachebust) {
  return request("GET", url, null, sameorigin, cachebust);
}

/**
 * @param {string} name
 * @returns {Promise<string>}
 */
export async function createBlog(name) {
  const response = await post("/api/blogs", { name }, true);

  if (response.status != 200) {
    throw new Error(
      `Unexpected response status code ${response.status} for blog creation`
    );
  }

  const data = await response.json();
  return data["blog_id"];
}

/**
 * @param {string} id
 * @param {boolean} cachebust
 * @returns {Promise<{
 *  name: string,
 *  posts: [{title: string, content: string}]
 * }?>}
 */
export async function getBlog(id, cachebust) {
  const response = await get(
    `https://picoblog-static-ae182846340bc2df.brics-ctf.ru/${id}.json`,
    false,
    cachebust
  );

  if (response.status == 404) {
    return null;
  } else if (response.status != 200) {
    throw new Error(
      `Unexpected response status code ${response.status} for blog retrieval`
    );
  }

  return response.json();
}

/**
 * @returns {Promise<{blogID: string}?>}
 */
export async function getUser() {
  const response = await get("/api/user", true, false);

  if (response.status == 401) {
    return null;
  } else if (response.status != 200) {
    throw new Error(
      `Unexpected response status code ${response.status} for user info retrieval`
    );
  }

  const data = await response.json();

  return { blogID: data["blog_id"] };
}

/**
 * @param {string} title
 * @param {string} content
 * @returns {Promise<void>}
 */
export async function createPost(title, content) {
  const response = await post("/api/posts", { title, content }, true);

  if (response.status != 200) {
    throw new Error(
      `Unexpected response status code ${response.status} for post creation`
    );
  }

  return;
}

/**
 * @returns {Promise<void>}
 */
export async function askForReview() {
  const response = await post("/api/review", {}, true);

  if (response.status != 200) {
    throw new Error(
      `Unexpected response status code ${response.status} for review`
    );
  }

  return;
}
