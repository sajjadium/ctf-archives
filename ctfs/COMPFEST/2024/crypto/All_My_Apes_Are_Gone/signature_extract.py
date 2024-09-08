import binascii
from bitcoin.core import CTransaction, CMutableTransaction
from bitcoin.core.script import SignatureHash, SIGHASH_ALL, CScript

#pip install ecdsa
#pip install 

def extract_msg_hash_and_sig(tx_hex):
    # Decode the transaction hex
    tx = CTransaction.deserialize(binascii.unhexlify(tx_hex))
    
    # Convert to mutable transaction to access scriptSig
    mtx = CMutableTransaction.from_tx(tx)
    
    # Extract scriptSig from the first input
    script_sig = mtx.vin[0].scriptSig
    
    print(f"ScriptSig: {script_sig.hex()}")
    
    # Parse the scriptSig
    sig = None
    pubkey = None
    script_elements = list(CScript(script_sig))
    
    if len(script_elements) >= 2:
        sig = script_elements[0]
        pubkey = script_elements[1]
    else:
        print("ScriptSig doesn't have the expected structure.")
    
    if sig is not None:
        if isinstance(sig, bytes):
            # Remove the last byte (sighash flag) from the signature
            sig = sig[:-1]
            print(f"Signature (hex): {sig.hex()}")
        else:
            print(f"Unexpected signature type: {type(sig)}")
            print(f"Signature (raw): {sig}")
    
    if pubkey is not None:
        if isinstance(pubkey, bytes):
            print(f"Public Key (hex): {pubkey.hex()}")
        else:
            print(f"Unexpected public key type: {type(pubkey)}")
            print(f"Public Key (raw): {pubkey}")
    
    # Calculate the sighash (message hash)
    sighash = SignatureHash(mtx.vout[0].scriptPubKey, mtx, 0, SIGHASH_ALL)
    
    return sighash.hex(), sig.hex() if isinstance(sig, bytes) else str(sig), pubkey.hex() if isinstance(pubkey, bytes) else str(pubkey)


tx_hex = ""
msg_hash, sig, pubkey = extract_msg_hash_and_sig(tx_hex)
print(f"msg_hash = {msg_hash}")
print(f"sig = {sig}")
print(f"pubkey = {pubkey}")