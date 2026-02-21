Aur0r4

Take all my money, I am very very rich hehe


A vault contract on Sui holds 10 billion tokens. Can you drain it?

## Your Goal

1. Study the vault contract
2. Find the vulnerability
3. Write an exploit module:
   - Create a file named `exploit.move`
   - Use the module name `solution::exploit`
   - Implement the `solve` function:
     `public fun solve(vault: &mut Vault, clock: &Clock, ctx: &mut TxContext)`

4. Submit your source code:
   - Connect to the server: `nc <host> <port>`
   - Enter the size of your `exploit.move` file in bytes (e.g., `670`).
   - Paste the entire source code of `exploit.move` when prompted.

## Win Condition

Drain at least 90% of the vault reserves (9 billion tokens).
