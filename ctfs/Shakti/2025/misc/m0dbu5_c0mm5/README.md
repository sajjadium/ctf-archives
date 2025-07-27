Given that the network uses the Modbus protocol and is based on the RS485 bus, when the master wishes to read sensor data, the slave receives the data packet as shown below. Send the master the slave's response, and suppose the slave data is 30. (decimal). Master requirements are 03 04 00 0A 00 04 70 09

flag format: ShaktiCTF{XX XX XX XX XX XX XX XX}
Flag Format:
ShaktiCTF{slave_response}
