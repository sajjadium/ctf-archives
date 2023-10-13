
class ExtendedMath {
    newMath = Math
    constructor() {
        this.newMath.seeds = [0.1, 0.2, 0.3, 0.4, 0.5];
        this.newMath.next = Math.seeds[new Date().getTime() % Math.seeds.length];
        this.newMath.random = function () {
            this.next = this.next * 3 + 1234;
            return (this.next / 65536) % 32767;
        };
    }
}
export default ExtendedMath;

