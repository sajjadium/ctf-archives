import dataclasses
import re
import secrets
import sys
from pyrage import passphrase  # type: ignore

args = sys.argv[1:]


def make_password(num_words):
    text = open("amontillado.txt").read()
    words = list(set(re.sub("[^a-z]", " ", text.lower()).split()))
    return "".join(secrets.choice(words) for _ in range(num_words))


@dataclasses.dataclass
class Node:
    letter: str
    id: int


@dataclasses.dataclass
class Edge:
    a: Node
    b: Node


@dataclasses.dataclass
class Graph:
    nodes: list[Node]
    edges: list[Edge]


class IdGen:
    def __init__(self):
        self.ids = set()

    def generate_id(self):
        while True:
            new_id = secrets.randbelow(1024**3)
            if new_id not in self.ids:
                self.ids.add(new_id)
                return new_id


def make_hint(password):
    graph = Graph([], [])
    idg = IdGen()
    random = secrets.SystemRandom()
    graph.nodes = [Node(letter, idg.generate_id()) for letter in password]
    edgelst = list(zip(graph.nodes, graph.nodes[1:]))
    for _ in range(len(password) * 3):
        edgelst.append(tuple(random.sample(graph.nodes, 2)))  # type: ignore
    graph.edges = [
        Edge(b, a) if random.random() % 2 else Edge(a, b) for a, b in edgelst
    ]
    random.shuffle(graph.nodes)
    random.shuffle(graph.edges)
    return graph


def encrypt(num_words, secret):
    password = make_password(num_words)
    print(password + f"  {len(password)}")
    graph = make_hint(password)
    with open("hint.txt", "w") as f:
        f.write(
            "\n".join([f"{n.id} [{n.letter}];" for n in graph.nodes])
            + "\n"
            + "\n".join([f"{e.a.id} -- {e.b.id};" for e in graph.edges])
        )
    with open("secret.txt", "wb") as f:
        f.write(passphrase.encrypt(secret.encode(), password))


def main():
    encrypt(int(args[0]), open("flag.txt").read())


if __name__ == "__main__":
    main()
