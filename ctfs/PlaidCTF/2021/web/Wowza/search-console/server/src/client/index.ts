export interface Fetcher {
    get<T>(url: string): Promise<T>;
    post<T, U = unknown>(url: string, body: U): Promise<T>;
}

export class Client {
    public site;
    public user;
    public auth;

    constructor(fetcher: Fetcher) {
        this.site = new SiteClient(fetcher);
        this.user = new UserClient(fetcher);
        this.auth = new AuthClient(fetcher);
    }
}

export namespace SiteClient {
    export type Site =
        | { domain: string, pending: false }
        | { domain: string, pending: true, validationCode: string }
        ;
}

export class SiteClient {
    constructor(private fetcher: Fetcher) {};

    public sites() {
        return this.fetcher.get<SiteClient.Site[]>("/site/");
    }

    public register(domain: string) {
        return this.fetcher.post<{}, { domain: string }>("/site/register", { domain });
    }

    public validate(domain: string) {
        return this.fetcher.post<{}, { domain: string }>("/site/validate", { domain });
    }

    public scrape(domain: string) {
        return this.fetcher.post<{}, { domain: string }>("/site/scrape", { domain });
    }
}

export class UserClient {
    constructor(private fetcher: Fetcher) {};

    public self() {
        return this.fetcher.get<{ username: string }>("/user/");
    }
}

export class AuthClient {
    constructor(private fetcher: Fetcher) {};

    public login(username: string, password: string) {
        return this.fetcher.post<{ username: string, password: string }>("/auth/login", { username, password });
    }

    public register(username: string, password: string) {
        return this.fetcher.post<{ username: string, password: string }>("/auth/register", { username, password });
    }

    public logout() {
        return this.fetcher.post<{}, {}>("/auth/logout", {});
    }
}