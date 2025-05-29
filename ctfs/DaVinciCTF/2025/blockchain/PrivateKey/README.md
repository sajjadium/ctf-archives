A thief sold a stolen artwork for cryptocurrencies, you are trying to track him. You need to find the private key of the wallet he used for the sale.

His phone was retrieved, here is what we found inside : The first wallet he created has this address 0xBB936f91EB631f6d1a376dBE203D22BA70337F7F, but he didn't use this one for the sale. He had created 2 wallets before the one he was using for the sale, using the same seedphrase. He took this picture named "Backup"

The solution is the private key hashed in md5 inside DVCTF{}

For example, if the private key is 0xdcae2f39a2e09978519003cf7a4cf5524d4d4486b1bef9e2bc5ebbcfbe394a26, the flag would be DVCTF{67bbecf3d7da21e86010576f912e62c6}
