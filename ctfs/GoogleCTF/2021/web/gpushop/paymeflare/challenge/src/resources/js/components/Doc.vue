<template>
<div>
<script ref="md" type="text/template">
paymeflare
===
Thank you for choosing *paymeflare*, the bleeding edge decentralized payment solution!

Integrating with paymeflare
---
Paymeflare acts as a reverse proxy. To add your host to *paymeflare* click on [Account](/account) and set the following items:
- Host: The domain paymeflare will manage.
- IP: Current IP and optional port of the service.

Please allow up to 5 minutes for the configuration to propagate.  
Then edit your dns domain and add a *CNAME* record pointing to **paymeflare.2021.ctfcompetition.com**.

Authentication
---
To verify that requests are coming from *paymeflare*, requests will have an `X-Pay` header with the secret value displayed on your account.

Checkout
---
Any request with a path matching `/checkout` will have an `X-Wallet` header added with the payment address. Provide this address to your customers for payment.  
These addresses are unique and independent so they can be associtated with a single order.  
Generated addresses can be found in your [Account](/account) page.

</script>
<div v-html="doc"></div>
</div>
</template>

<script>
import marked from 'marked';

export default {
    data() {
        return {
            doc: '',
        }
    },
    mounted() {
        console.log(this.$refs)
        this.doc = marked(this.$refs.md.innerText);
        console.log(this.doc)
    }
}

</script>
