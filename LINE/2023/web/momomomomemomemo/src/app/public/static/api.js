const { fetch, sha256 } = window;

class GraphQL {
    constructor(host, option = {}) {
        this.endpoint = host + "/";
        this.endpoint += option.path || "graphql";
    }

    get token() {
        return localStorage.getItem("token");
    }

    set token(token) {
        localStorage.setItem("token", token);
    }

    async #getQueryHash(query) {
        return sha256(query);
    }

    #mutation(query) {
        return fetch(this.endpoint, {
            method: "POST",
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify({ query }),
        });
    }

    async #query(query) {
        const hash = await this.#getQueryHash(query);
        const res = await fetch(
            this.endpoint +
                "?" +
                new URLSearchParams({
                    extensions: JSON.stringify({
                        persistedQuery: { version: 1, sha256Hash: hash },
                    }),
                }),
            {
                headers: { "Content-type": "application/json" },
            }
        );
        const data = await res.clone().json();
        if (data.errors) {
            if (data.errors[0].extensions.code == "PERSISTED_QUERY_NOT_FOUND") {
                return await fetch(this.endpoint, {
                    method: "POST",
                    headers: { "Content-type": "application/json" },
                    body: JSON.stringify({
                        query,
                        extensions: {
                            persistedQuery: {
                                version: 1,
                                sha256Hash: hash,
                            },
                        },
                    }),
                });
            }
        }
        return res;
    }

    register(username, password) {
        const query = `mutation { 
            register (
                username: "${username}", 
                password: "${password}")
            }`;
        return this.#mutation(query);
    }

    login(username, password) {
        const query = `mutation { 
            login(
                username: "${username}", 
                password: "${password}"
                )
            }`;
        return this.#mutation(query);
    }

    memos() {
        const query = `query { 
            memos (
                token: "${this.token}"
                ) {
                    id 
                    ownerId 
                    content
                } 
            }`;
        return this.#query(query);
    }

    memo(id) {
        const query = `query { 
            memo (
                id: "${id}", 
                token: "${this.token}") {
                    content
                } 
            }`;
        return this.#query(query);
    }

    addMemo(content) {
        const query = `mutation { 
            addMemo (
                token: "${this.token}", 
                content: "${content.replaceAll("\n", "\\n")}")
            }`;
        return this.#mutation(query);
    }

    reportBug(url, captchaCode) {
        const query = `mutation { 
            reportBug (token: "${this.token}", 
            url: "${url}", 
            captchaCode: "${captchaCode}") 
        }`;
        return this.#mutation(query);
    }

    getCaptchaImage() {
        const query = `mutation { 
            getCaptchaImage(
                token: "${this.token}") 
            }`;
        return this.#mutation(query);
    }
}

export default GraphQL;
