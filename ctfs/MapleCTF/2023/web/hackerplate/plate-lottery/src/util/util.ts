import http from 'http';
import querystring from 'querystring';
import { VALID_LETTERS, VALID_NUMBERS } from './constants.js';

export function randomIndices(arraySize: number, numIndices: number): number[] {
    // let the client floor it
    return Array.from(
        { length: numIndices }, () => Math.random() * arraySize);
}

export function generateRandomPlate(): string {
    // format: L-DDD-LL, where L is letter, D is digit
    // every plate this year starts with L
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
    const digits = "0123456789".split("");
    return `L-${grc(digits)}${grc(digits)}${grc(digits)}-${grc(letters)}${grc(letters)}`;
}

function grc(charset: string[]): string {
    // get random character
    return charset[Math.floor(Math.random() * charset.length)];
}

export function isValidVIN(vin: string): boolean {
    const validCharset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".split("");
    return typeof vin === "string" && vin.length === 17 && vin.split("").every((c) => validCharset.includes(c));
}

export function makeRequest(url: string, method: string, data: any): Promise<any> {
    return new Promise((resolve, reject) => {
        const req = http.request(url, { method: method }, (res) => {
            let body = '';
            res.on('data', (chunk) => {
                body += chunk;
            });
            res.on('end', () => {
                if (res.statusCode === 200) {
                    resolve(body);
                } else {
                    reject(body);
                }
            });
        });
        req.on('error', (err) => {
            reject(err);
        });
        if (data) {
            // write as form data
            req.setHeader('Content-Type', 'application/x-www-form-urlencoded');
            req.write(new URLSearchParams(data).toString());
        }
        req.end();
    });
}

function permutation(charset, length): string[] {
    const permutations: string[] = []
    const permutationHelper = (charset: string[], length: number, permutation: string) => {
        if (permutation.length === length) {
            permutations.push(permutation)
            return
        }
        for (let i = 0; i < charset.length; i++) {
            permutationHelper(charset, length, permutation + charset[i])
        }
    }
    permutationHelper(charset, length, "")
    return permutations
}

export function getPlatePossibilitySpace(platesToIgnore: number[]): number[] {
    // new year new L's

    let arr = Array.from({ length: 10 ** 3 * 26 ** 2 }, (_, i) => i);
    for (let i = 0; i < platesToIgnore.length; i++) {
        arr[platesToIgnore[i]] = -1;
    }
    return arr.filter((x) => x !== -1);

    // const plates: string[] = []
    // const startingLetter = "L"
    // const numCombinations: string[] = permutation(VALID_NUMBERS, 3)
    // const charCombinations: string[] = permutation(VALID_LETTERS, 2)
    // for (let i = 0; i < numCombinations.length; i++) {
    //     for (let j = 0; j < charCombinations.length; j++) {
    //         let plate: string = startingLetter + "-" + numCombinations[i] + "-" + charCombinations[j]
    //         if (platesToIgnore.indexOf(plate) === -1) {
    //             plates.push(plate);
    //         }
    //     }
    // }
    // return plates;
}

export function findPlateFromIndex(index: number, platesToIgnore: number[]) {
    // we know the plates to ignore are sorted... find how many of the elements are less than index
    let numLessThanIndex = 0;
    for (let i = 0; i < platesToIgnore.length; i++) {
        if (platesToIgnore[i] < index) {
            numLessThanIndex++;
        }
    }
    let tempIndex = index + numLessThanIndex;
    const ords = [];
    for (let i = 0; i < 2; i++) {
        ords.push(tempIndex % 26);
        tempIndex = Math.floor(tempIndex / 26);
    }
    for (let i = 0; i < 3; i++) {
        ords.push(tempIndex % 10);
        tempIndex = Math.floor(tempIndex / 10);
    }
    return "L" + "-" + ords[4] + ords[3] + ords[2] + "-" + String.fromCharCode(ords[1] + 65) + String.fromCharCode(ords[0] + 65);
}