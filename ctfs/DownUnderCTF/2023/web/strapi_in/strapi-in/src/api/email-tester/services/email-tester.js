module.exports = {
    sendTestEmail: async (templateRef) => {
        await strapi
            .plugin('email-designer')
            .service('email')
            .sendTemplatedEmail(
                {
                    to: "recipient@strapi.in",
                    from: "sender@strapi.in",
                    replyTo: "sender@strapi.in",
                    attachments: []
                },
                {
                    templateReferenceId: templateRef,
                    subject: "Test Email"
                },
                {}
            )
    }
}