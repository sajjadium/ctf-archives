A mysterious distributor is offering a free supply of "Power" – a pill that grants various superpowers for five minutes. This distributor communicates with his contacts using a custom-made special device.

By a truly unbelievable coincidence, you were recently out for a walk when you saw a small package fall off a truck ahead of you. Inside, you found the latest version of some forensics software, a hardware dongle designed to prevent piracy, a bizarrely large number of cable adapters, an oscilloscope and the custom communication device!

After inspecting the device, you learn that it simply uses AES-128 ECB for encryption. However, you don't have the key. Using the oscilloscope, you are able to extract voltage measurements for the state right after the call to sub_bytes in the AES algorithm:

state = plaintext
add_round_key(state, ...)

for i in 1..n:
   sub_bytes(state)
                   <-- Volatage measurements of state
   shift_rows(state)
   mix_columns(state)
   add_round_key(state, ...)

sub_bytes(state)
shift_rows(state)
add_round_key(state, ...)

Can you find the key and decrypt the secret message?
