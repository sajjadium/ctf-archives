export let modPrime = 0xffffffffffffffffffffffffffffff61n;
export let powerPrime = 0xd30a1674117779a3n;

export const setSpecialPrime = (n: bigint) => modPrime = n;
export const setPowerPrime = (n: bigint) => powerPrime = n;


const myHashFunction = (data: Buffer) => {
    let currentHash: bigint = 0n;

    for (let i = 0n; i < data.byteLength; i++) {
        const byte = data[Number(i)];

        currentHash ^= (powerPrime ** BigInt(byte) * i) % modPrime;
    }

    return currentHash;
};

export default myHashFunction;
