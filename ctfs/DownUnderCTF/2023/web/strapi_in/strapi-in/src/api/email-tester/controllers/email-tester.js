module.exports = {
    sendTestEmail: async (ctx, next) => {
        try {
            const { refId } = ctx.params;
            await strapi
                .service("api::email-tester.email-tester")
                .sendTestEmail(refId);
            ctx.body = {msg:"Sent!"}
        } catch (err) {
            console.error(err);
            ctx.badRequest("Error sending test email", {moreDetails: err});
        }
    }
}