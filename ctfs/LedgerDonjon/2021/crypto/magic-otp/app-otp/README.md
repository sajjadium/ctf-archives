## Magic OTP

This app can be built in one of 2 modes: client or server.

- The server app is installed on a single hardware device.
- The client app is installed on a fleet of hardware devices, initialized with
  unique seeds and distributed to users.

The administrator registers each client device (using its public key) on the
server. Once registered, client devices can request OTPs from the server.

The server device contains an OTP secret which can be easily rotated if it were
to be compromised. This OTP secret is embedded in any piece of software that are
used to check the validity of an OTP.

The public key of a client device can be revoked if a user loses its device.


### Build

```console
make clean MODE=CLIENT
make MODE=CLIENT && cp bin/app.elf /tmp/app-client.elf
make clean MODE=SERVER
make MODE=SERVER && cp bin/app.elf /tmp/app-server.elf
mv /tmp/*.elf bin/
```


### Usage

Run the server:

```console
speculos.py --api-port 5000 --seed "lake essence common federal aisle amazing spend danger suspect barely verb try" ./bin/app-server.elf
```

Run the client:
```console
speculos.py --api-port 6000 --apdu-port 6001 --seed "wire solve theme picnic matter aunt light volcano time bright produce verify" ./bin/app-client.elf
```

Or use the `demo.py` script using the latest version of speculos,
[1ff15147de4c6ea278c7cde9be34a0feb10fffdd](https://github.com/LedgerHQ/speculos/tree/1ff15147de4c6ea278c7cde9be34a0feb10fffdd).
