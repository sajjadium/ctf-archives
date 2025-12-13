const crypto = require('crypto');

function solveProofOfWork(challenge, difficulty) {
    let nonce = 0;
    while (true) {
        const hash = crypto.createHash('sha256')
            .update(challenge + nonce.toString())
            .digest('hex');
        
        if (hash.startsWith('0'.repeat(difficulty))) {
            console.log(`Hash: ${hash}`);
            return nonce.toString();
        }
        
        nonce++;
        if (nonce % 100000 === 0) {
            console.log(`Tried ${nonce} solutions...`);
        }
    }
}

// Get challenge and difficulty from command line arguments
const challenge = process.argv[2];
const difficulty = parseInt(process.argv[3]);

if (!challenge || !difficulty) {
    console.error('Please provide both challenge and difficulty');
    console.error('Usage: node solve_pow.js <challenge> <difficulty>');
    console.error('Example: node solve_pow.js abc123 4');
    process.exit(1);
}

console.log('Challenge:', challenge);
console.log('Difficulty:', difficulty);
console.log('Solving...');

const startTime = Date.now();
const solution = solveProofOfWork(challenge, difficulty);
const endTime = Date.now();

console.log('\nSolution found!');
console.log('Nonce:', solution);
console.log('Time taken:', ((endTime - startTime) / 1000).toFixed(2), 'seconds');

// Verify the solution
const verificationHash = crypto.createHash('sha256')
    .update(challenge + solution)
    .digest('hex');
