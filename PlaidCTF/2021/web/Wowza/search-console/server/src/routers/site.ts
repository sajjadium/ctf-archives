import { marshalBody, Router } from "@zensors/expedite";
import { M } from "@zensors/sheriff";

import { Site } from "../state";
import { requireLogin } from "../state/user";
import { domainIsNotLocalhost, getTextRecords, MDomain, SafeError } from "../utils";

export const siteRouter = (new Router())
    .then(requireLogin);

siteRouter.get("/")
    .return((req) => Site.getSitesForUser(req.user.username))

siteRouter.post("/register/")
    .then(marshalBody(M.obj({ domain: MDomain })))
    .return<{ validationCode: string }>(async (req) => {
        const isSafe = await domainIsNotLocalhost(req.body.domain);
        if (!isSafe) {
            throw new Error("Invalid domain");
        }
        const validationCode = await Site.registerSite(req.user.username, req.body.domain);
        return { validationCode };
    });

siteRouter.post("/validate/")
    .then(marshalBody(M.obj({ domain: MDomain })))
    .return<{}>(async (req) => {
        const pendingSites = await Site.getPendingSitesForOwner(req.user.username);
        const site = pendingSites.find(({ domain }) => domain === req.body.domain);
        if (!site) {
            throw new SafeError(401, "Unable to find site")
        }

        const records = await getTextRecords(req.body.domain);
        const validationRecord = records.find((record) => record.startsWith("wowza-domain-verification="))
        const [_prefix, verification_code] = validationRecord?.split("=") ?? [];
        await Site.validateSite(req.user.username, req.body.domain, verification_code);

        return {};
    });

siteRouter.post("/scrape/")
    .then(marshalBody(M.obj({ domain: MDomain })))
    .return<{}>(async (req) => {
        await Site.scrapeSite(req.body.domain);
        return {};
    });
