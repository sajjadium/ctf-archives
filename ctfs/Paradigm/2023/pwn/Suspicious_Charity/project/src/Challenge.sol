contract Challenge {
    address public immutable ROUTER;

    constructor(address router) {
        ROUTER = router;
    }
}
