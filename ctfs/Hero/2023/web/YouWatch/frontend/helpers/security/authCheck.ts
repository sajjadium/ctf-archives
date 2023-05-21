import api from "../utils/api";

export default async function authCheck(ctx, authRoute) {
    const { req, res } = ctx; 
    const profile = await api("GET", "/api/profile", {}, req.headers.cookie, true);

    if (!authRoute && !profile.error) {
        res.setHeader("location", "/");
        res.statusCode = 302;
        res.end();
        return true;
    }

    if (authRoute && profile.error) {
        res.setHeader("location", "/login");
        res.statusCode = 302;
        res.end();
        return true;
    }

    return false;
}