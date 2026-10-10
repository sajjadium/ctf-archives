Task author RU

В соседней лаборатории решили не связываться со стандартными кривыми и выкатили собственную — 256-битную, в стиле secp256k1, со своим простым и своей компактной арифметикой, «без лишних проверок, точки же всё равно свои». Капибара заглянула в код и хмыкнула: координаты класс хранит, а спросить, лежат ли они вообще на кривой, забыли. Вам достались исходник и данные одного сеанса: несколько диагностических точек, для каждой — результат операции над секретным ключом, и зашифрованный флаг. Восстановите секрет.

EN

A neighbouring lab decided not to bother with standard curves and shipped their own — a 256-bit, secp256k1-style curve with its own prime and its own compact arithmetic, "no needless checks, the points are all ours anyway". A capybara skimmed the code and smirked: the class stores coordinates but never asks whether they lie on the curve at all. You have the source and one session's data: a handful of diagnostic points, each with the result of an operation using the secret key, plus an encrypted flag. Recover the secret.
