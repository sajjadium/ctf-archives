const sleep = (ms) => new Promise((resolve, reject) => {
    setTimeout(resolve, ms);
});

export class BankClass {
    constructor() {
        this.customers = Object.create(null);
    }
    async getMoney(customer) {
        if (!Object.hasOwn(this.customers, customer)) {
            this.customers[customer] = { money: 0 };
        }
        await sleep(1000); // for security purposes
        return this.customers[customer].money;
    }
    async addMoney(customer, deposit) {
        const money = await this.getMoney(customer);
        return this.customers[customer].money = money + deposit;
    }
};
