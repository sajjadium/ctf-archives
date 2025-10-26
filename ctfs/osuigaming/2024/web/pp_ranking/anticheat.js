const THREE_MONTHS_IN_MS = 3 * 30 * 24 * 60 * 1000;

const anticheat = (user, newPP) => {
    const pp = parseInt(newPP);
    if (user.playCount < 5000 && pp > 300) {
        return true;
    }

    if (+new Date() - user.registerDate < THREE_MONTHS_IN_MS && pp > 300) {
        return true;
    }

    if (+new Date() - user.registerDate < THREE_MONTHS_IN_MS && pp + user.performance > 5_000) {
        return true;
    }

    if (user.performance < 1000 && pp > 300) {
        return true;
    }

    return false;
};

export default anticheat;