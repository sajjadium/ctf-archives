
(function() {
    new Vue({
        el: '#app',
        data: {
            dropdownVisibility: {
                source: false,
                target: false
            },
            sourceCoinAmount: 0,
            sourceCoinFilter: '',
            targetCoinFilter: '',
            sourceCoinValue: 'cashout',
            targetCoinValue: 'ascoin',
            balances: [],
            coins: [],
            club: false
        },
        methods: {
            changeSourceCoin(name) {
                this.sourceCoinValue = name;
                this.dropdownVisibility.source = false;
                this.sourceCoinFilter = '';
            },
            changeTargetCoin(name) {
                this.targetCoinValue = name;
                this.dropdownVisibility.target = false;
                this.targetCoinFilter = '';
            },
            swapCoins() {
                const tmp = this.sourceCoinValue;
                this.sourceCoinValue = this.targetCoinValue;
                this.targetCoinValue = tmp;
            },
            fetchCoins() {
                fetch("/api/fetch_coins").then(res => res.json()).then(coins => {
                    this.coins = coins;
                })
            },
            fetchBalances() {
                fetch("/api/wallet/balances").then(res => res.json()).then(balances => {
                    this.balances = balances;
                })
            },
            convert() {
                fetch("/api/wallet/transaction", {
                    method: "POST",
                    body: JSON.stringify({
                        sourceCoin: this.sourceCoinValue,
                        targetCoin: this.targetCoinValue,
                        balance: this.sourceCoinAmount
                    }),
                    headers: {
                        "Content-Type": "application/json"
                    }
                }).then(_ => {
                    this.fetchBalances();
                    this.sourceCoinAmount = 0;
                })
            },
            joinGlacierClub() {
                fetch("/api/wallet/join_glacier_club", {method: "POST"}).then(res => res.json()).then(club => {
                    this.club = club;
                    this.$refs.modalGlacierclub.classList.add('is-active')
                })
            },
            closeClubModal() {
                this.$refs.modalGlacierclub.classList.remove('is-active')
            }
        },
        computed: {
            filteredSourceCoins() {
                return this.coins.filter(coin => coin.value.includes(this.sourceCoinFilter) && coin.name !== this.targetCoinValue);
            },
            filteredTargetCoins() {
                return this.coins.filter(coin => coin.value.includes(this.targetCoinFilter) && coin.name !== this.sourceCoinValue);
            },
            sourceCoin() {
                return this.coins.filter(coin => coin.name === this.sourceCoinValue)[0];
            },
            targetCoin() {
                return this.coins.filter(coin => coin.name === this.targetCoinValue)[0];
            }
        },
        mounted() {
            this.fetchCoins();
            this.fetchBalances();
        },
        delimiters: ['$$', '$$'],
    })
})();

(function() {
    setInterval(_ => {
        document.querySelectorAll("[data-adjust-width-to]").forEach(element => {
            const referenceElementId = element.dataset.adjustWidthTo;
            if(!referenceElementId) return; 
            const referenceElement = document.getElementById(referenceElementId);
            if(!referenceElement) return;
            element.style.width = `${referenceElement.offsetWidth}px`;
        })    
    })
})();