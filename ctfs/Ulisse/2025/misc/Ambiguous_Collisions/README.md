misc grammars
Pietro Bertozzi <@Pietro>

Have you ever wondered how a programming language works? First, you need to become familiar with the concepts of scope, production, terminal symbol, and non-terminal symbol. If you understand the following, then you are ready.

S -> A
A -> C | ABA
B -> +
C -> a

S -> A -> ABA -> CBA -> aBA -> a+A -> a+C -> a+a
