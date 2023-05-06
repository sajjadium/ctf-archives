const Permissions = {
    VERIFIED: 'verified',
};

function hasPermission(userPermissions, username, permission) {
    return userPermissions.get(username)?.includes(permission) ?? false;
}

function authz({ userPermissions, routePermissions }) {
    return (req, res, next) => {
        const { username } = req.user;
        for (const [regex, permission] of routePermissions) {
            if (regex.test(req.url) && !hasPermission(userPermissions, username, permission)) {
                return res.status(403).send('forbidden');
            }
        }
        next();
    };
}

module.exports = {
    Permissions,
    authz,
};
