Боб использует генератор псевдослучайных чисел, который основан на возведении в степень. Его формула:

Xn = pn mod m, n >= 0, 0 < p, m < 10000

Докажите, что он тоже небезопасен и непригоден для криптографического использования .

Допустим, вы смогли перехватить последовательные числа, когорые создал генератор. Взломайте его. Для этого достаточно найти его параметры p и m и предсказать следующее псевдослучайное число.

Флаг в формате grodno{p;m;next_number}

Bob uses a pseudorandom number generator that is based on exponentiation. Its formula:

Xn = pn mod m, n >= 0, 0 < p, m < 10000

Prove that it too is insecure and unsuitable for cryptographic use.

Let's say you were able to intercept the sequential numbers that the generator created. Hack it. To do this, it is enough to find its parameters p and m and predict the next pseudo-random number.

Flag in the format grodno{p;m;next_number}
