function getPaymentURL(cartId){
    throw new Error('Payment Processor is down due to ransomware. Please try again later')
}

let discountCodes =  {
    "FREEZTUFSSZ1412": 100
}

function validateDiscount(discountCode) {
    return (discountCodes[discountCode] ?? 0) / 100
}

module.exports = { 
    getPaymentURL,
    validateDiscount,
};