ElGamal is stuck on this problem. Can you help him solve it?

P = 2147483647 ; a * da = 335007430212 ; c2 = [782609095, 956334224, 948802740, 27994553, 1649557991, 1242339631, 2047940013, 1044206616, 758980367, 542738157, 1732201892, 196836220, 193577195, 649932019, 1925903078, 862766676];

da is related to P in the same way that a is Public key : {P, a, b} Private key = da ; b = (a ^ da) mod P; c1 = (a^r) mod P, where r is a random integer calculated by the following loop: 2 < r < (len(c2)+2)
