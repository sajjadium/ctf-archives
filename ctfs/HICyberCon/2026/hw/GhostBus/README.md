by Hidden Investigations
hardware
A smart-lock sensor hub was pulled from a decommissioned site. The vendor insists the secure element is locked and the sealed region cannot be read. A field engineer probed the hub's internal UART bus between the MCU and the secure element, and separately dumped the hub's external SPI NOR flash. The external flash also holds a recovery copy of the MCU firmware; firmware.elf is supplied separately for analysis.

The secure element holds a nonce for the currently provisioned sealed record. It returns the same nonce on each read; reprovisioning replaces both that nonce and the sealed ciphertext. This is not a fresh-random-number command.

Recover the hidden read, reverse the key derivation and open the sealed region. No brute force needed: all crypto is standard, and every byte you need is in the provided evidence.
