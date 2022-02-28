function access(r) {
    var whitelist = [
        "eth_blockNumber",
        "eth_call",
        "eth_chainId",
        "eth_estimateGas",
        "eth_gasPrice",
        "eth_getBalance",
        "eth_getCode",
        "eth_getTransactionByHash",
        "eth_getTransactionCount",
        "eth_getTransactionReceipt",
        "eth_sendTransaction",
        "eth_sendRawTransaction",
        "net_version",
        "rpc_modules",
        "web3_clientVersion"
    ];

    try {
        var payload = JSON.parse(r.requestBody);
        if (payload.jsonrpc !== "2.0") {
            r.return(401, "jsonrpc version not supported\n");
            return;
        }
        if (!whitelist.includes(payload.method)) {
            r.return(401, "jsonrpc method is not allowed\n");
            return;
        }
        if (Object.keys(payload).filter(key => key.toLowerCase() === 'method').length > 1) {
            r.return(401, "jsonrpc method is not allowed\n");
            return;
        }
    } catch (error) {
        r.return(415, "Cannot parse payload into JSON\n");
        return;
    }

    r.internalRedirect('@jsonrpc');
}

export default { access }
