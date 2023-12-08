export default (controller) => async (req, res, next) => {
    try {
        await controller(req, res, next);
    } catch (err) {
        return res.render("robot", {
            error: err.message ?? "Something went wrong",
        });
    }
};
