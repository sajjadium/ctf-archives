Time to learn some post-quantum crypto!

The signing procedure of Dilithium uses rejection sampling to generate a signature, and the authors give the following reasoning:

“If
z
z were directly output at this point, then the signature scheme would be insecure due to the fact that the secret key would be leaked. To avoid the dependency of
z
z on the secret key, we use rejection sampling. […] The first check is necessary for security, while the second is necessary for both security and correctness.” [1]

Now, it’s your task to prove this.

diff --git a/ref/sign.c b/ref/sign.c
index 7d3f882..39fbad2 100644
--- a/ref/sign.c
+++ b/ref/sign.c
@@ -158,7 +158,7 @@ rej:
   polyvecl_invntt_tomont(&z);
   polyvecl_add(&z, &z, &y);
   polyvecl_reduce(&z);
-  if(polyvecl_chknorm(&z, GAMMA1 - BETA))
+  if(!polyvecl_chknorm(&z, GAMMA1 - BETA))
     goto rej;

   /* Check that subtracting cs2 does not change high bits of w and low bits
⚠️ Warning: We provide the complete source code running on the server and a docker-compose.yml file for local testing. Please solve the challenge locally before starting a remote instance. If your solution does not work locally, there is no point in trying it on remote. Not only do you have debug capabilities on a local deployment, generating the signatures only if you need them also spreads out the resource spikes for us, increasing your chances of stable infra ;) So please avoid using remote until you have a verified working solution.

[1]: Shi Bai, Léo Ducas, Eike Kiltz, Tancrède Lepoint, Vadim Lyubashevsky, Peter Schwabe, Gregor Seiler, and Damien Stehlé.CRYSTALS-dilithium, algorithm specifications and supporting documentation, 2021. https://pq-crystals.org/dilithium/data/dilithium-specification-round3-20210208.pdf.

(dilithium disapproves): z_inf >= gamma_1 - beta / (dilithium approves): z_inf < gamma_1 - beta
