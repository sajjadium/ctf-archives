import path from "path";

const preTask = (solution) => {
    if (typeof solution !== "string") {
        throw new Error("Solution must be a string");
    }
    if (solution.length > 512) {
        throw new Error("Solution must be less than 512 characters");
    }
    if (solution === "flag") {
        throw new Error("Your solution can't be 'flag'");
    }
    if (solution === "./flag") {
        throw new Error("Your solution can't be './flag'");
    }
};

export const task1 = (solution) => {
    preTask(solution);
    if (!solution.startsWith("/robot") || solution.endsWith("/flag")) {
        throw new Error(
            "You cannot access the flag!!! You are UNAUTHORIZED!!! 🤖🤖🤖🤖🤖"
        );
    }

    const solutionPath = path.join("/", solution);
    return solutionPath === "/flag";
};

export const task2 = (solution) => {
    preTask(solution);
    solution = solution.replaceAll("../", "");
    if (solution === "/flag") {
        throw new Error(
            "You cannot ACCESS the flag!!! You are UNAUTHORIZED!!! 🤖🤖🤖🤖🤖"
        );
    }

    const solutionPath = path.join("/", solution);
    return solutionPath === "/flag";
};

export const task3 = (solution) => {
    preTask(solution);
    if (solution.includes("../") || solution === "/flag") {
        throw new Error(
            "You CANNOT ACCESS the flag!!! You are UNAUTHORIZED!!! 🤖🤖🤖🤖🤖"
        );
    }

    const solutionPath = path.join("/", solution);
    return solutionPath === "/flag";
};

export const tasks = [
    `if (!solution.startsWith("/robot") || solution.endsWith("/flag")) {
    throw new Error(
        "You cannot access the flag!!! You are UNAUTHORIZED!!! 🤖🤖🤖🤖🤖"
    );
}

const solutionPath = path.join("/", solution);
return solutionPath === "/flag";`,
    `solution = solution.replaceAll("../", "");
    if (solution === "/flag") {
        throw new Error(
            "You cannot ACCESS the flag!!! You are UNAUTHORIZED!!! 🤖🤖🤖🤖🤖"
        );
    }

    const solutionPath = path.join("/", solution);
    return solutionPath === "/flag";`,
    `if (solution.includes("../") || solution === "/flag") {
    throw new Error(
        "You CANNOT ACCESS the flag!!! You are UNAUTHORIZED!!! 🤖🤖🤖🤖🤖"
    );
}

const solutionPath = path.join("/", solution);
return solutionPath === "/flag";`,
];
