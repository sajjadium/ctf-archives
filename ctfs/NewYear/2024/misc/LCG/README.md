Линейный конгруэнтный генератор (ЛКГ) - это метод генерации псевдослучайных чисел. Его работа описывается формулой:

Xn+1 = (a * Xn + c) mod m, n >= 0
X0 = const

Важно помнить, что ЛКГ неисправимо небезопасен и совершенно непригоден для криптографического использования .

Допустим, вы смогли перехватить последовательные числа, когорые создал ЛКГ. Докажите что он не безопасен, взломав ЛКГ. Для этого достаточно найти его параметры a, c, m и предсказать следующее псевдослучайное число.

Флаг в формате grodno{a;c;m;next_number}

Linear congruent generator (LCG) is a method for generating pseudorandom numbers. Its work is described by the formula:

Xn+1 = (a * Xn + c) mod m, n >= 0
X0 = const

It is important to remember that LCG is incorrigibly insecure and completely unsuitable for cryptographic use.

Let's say you were able to intercept the sequential numbers that LCG created. Prove that it is not safe by hacking LCG. To do this, it is enough to find its parameters a, c, m and predict the next pseudo-random number.

Flag in the format grodno{a;c;m;next_number}
