import * as anchor from "@project-serum/anchor";
import { Program } from "@project-serum/anchor";
import { Chall } from "../target/types/chall";

describe("chall", () => {
  // Configure the client to use the local cluster.
  anchor.setProvider(anchor.AnchorProvider.env());

  const program = anchor.workspace.Chall as Program<Chall>;
  const authority = (program.provider as anchor.AnchorProvider).wallet;

  it("Is initialized!", async () => {
    // Add your test here.
    const counter = anchor.web3.Keypair.generate();
    const tx = await program.methods.initialize()
      .accounts({
        counter: counter.pubkey,
        authority: authority.pubkey
      })
      .rpc();
    console.log("Your transaction signature", tx);
  });
});
