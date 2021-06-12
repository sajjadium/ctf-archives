export default function generatePasscode() {
    const chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"];
    for (let i = 0; i < chars.length - 1; i++) {
        let temp = chars[i];
        let j = Math.floor(Math.random() * (chars.length - i)) + i;
        chars[i] = chars[j];
        chars[j] = temp;
    }
    return chars.join("");
}