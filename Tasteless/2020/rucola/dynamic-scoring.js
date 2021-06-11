let console = safe_require('console');

console.log(ratings);

const minimum = 1;
const initial = 500;
const decay = 2;

for (const challenge of ratings) {
    const solve_count = challenge.solves.size;
    challenge.points = ((minimum - initial) / (decay * decay)) * (solve_count * solvecount) + initial;
}


ratings;