export function quad(x: number, y: number, x2: number, y2: number) {
    return [
        x, y, x2, y, x2, y2,
        x, y, x2, y2, x, y2
    ];
}
