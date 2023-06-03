export class TickScheduler {
    private minInterval: number;
    private maxInterval: number;
    lastUpdate: number = 0;
    timeSum: number = 0;

    constructor(minRatePerSec: number, maxRatePerSec: number) {
        this.minInterval = 1000 / maxRatePerSec;
        this.maxInterval = 1000 / minRatePerSec;
    }

    reset() {
        this.lastUpdate = performance.now();
    }

    getTickCount() {
        const now = performance.now();
        this.timeSum += now - this.lastUpdate;
        this.lastUpdate = now;

        if (this.timeSum < this.minInterval * 0.5)
            return 0;
        if (this.timeSum < this.maxInterval * 2.5) {
            this.timeSum = Math.min(this.timeSum - this.minInterval, 0);
            return 1;
        }

        const resMinTicks = Math.ceil(this.timeSum / this.minInterval);
        const resMaxTicks = Math.floor(this.timeSum / this.maxInterval);
        if (resMaxTicks !== resMinTicks + 1) {
            this.timeSum = 0;
            return resMaxTicks;
        }

        const resTicks = resMaxTicks;
        this.timeSum -= resTicks * this.maxInterval;
        return resTicks;
    }
}
