module.exports = {
    routes: [
        {
            method: 'GET',
            path: '/sendtestemail/:refId',
            handler: 'email-tester.sendTestEmail',
            config: {
                auth: false
            },
        },
    ],
};
  