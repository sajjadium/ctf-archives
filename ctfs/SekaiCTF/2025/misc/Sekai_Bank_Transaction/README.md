SEKAI
Mobile
Let me introduce you to Sekai Bank!

Notes: This is an Android Exploitation challenge that requires you to create an exploit application (.apk). Once you have created a working exploit, please submit it to POC Tester below. It is recommended that you verify the exploit works locally before submitting. Please make sure to build your POC with minSdkVersion set to 31 or lower.

Objectives: You need to steal one million from the user admin, which is the Sekai Bank user that the POC Tester is authenticated with. Please refrain from performing penetration testing on the backend, as it will yield no results; this is a pure Android Exploitation challenge. The flag will be displayed in the transaction history if your exploitation was successful.

POC Tester Flow:

Vuln App (Sekai Bank) will be launched.
It will authenticate as user admin and create two transactions. The first transaction is an instant transaction, and the second one is a delayed transaction (will be sent within 5 minutes after the transaction is placed).
Exploit App (Your POC) will be launched.
Your POC will have up to 5 minutes to run the exploit.
The final screenshot will be provided in the POC Tester.
Author: Marc
