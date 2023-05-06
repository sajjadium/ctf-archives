import { GraphQLError } from "graphql";
import jwt from "jsonwebtoken";
import captcha from "trek-captcha";

const APP_BASEURL = process.env.APP_BASEURL || "http://localhost:4000/";

const reportBug = async (_parent, { token, url, captchaCode }, context) => {
    const decoded = verifyJWT(token);

    let captcha;
    try {
        captcha = await context.dataSources.db.getCaptchaCode(decoded.sub);
    } catch (err) {
        console.error(err);
        throw new GraphQLError("reportBug failed");
    }

    if (
        (captcha.code && !(captchaCode === captcha.code)) ||
        !url.startsWith(APP_BASEURL)
    )
        throw new GraphQLError("reportBug failed");

    await context.dataSources.db.setCaptchaCode(decoded.sub, null);

    const urlWithoutOrigin = url.replace(new URL(url).origin, "");

    console.log(`reportBug (${decoded.sub}, ${urlWithoutOrigin})`);

    try {
        await context.dataSources.redis.rpush("report", urlWithoutOrigin);
        await context.dataSources.redis.incr("reported_count");
    } catch (err) {
        console.error(err);
        throw new GraphQLError("reportBug failed");
    }

    return true;
};

const getCaptchaImage = async (_parent, { token }, context) => {
    const decoded = verifyJWT(token);

    let captchaImage;
    try {
        const { token, buffer } = await captcha({ size: 6 });
        await context.dataSources.db.setCaptchaCode(decoded.sub, token);
        captchaImage = "data:image/gif;base64," + buffer.toString("base64");
    } catch (err) {
        console.error(err);
        throw new GraphQLError("getCaptcha failed");
    }

    return captchaImage;
};

const verifyJWT = (token) => {
    try {
        return jwt.verify(token, process.env.SECRET_KEY || "secretkey");
    } catch (err) {
        console.error(err);
        throw new GraphQLError("invalid token", {
            extensions: {
                code: "UNAUTHORIZED",
            },
        });
    }
};

export default {
    reportBug,
    getCaptchaImage,
};
