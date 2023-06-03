#!/usr/bin/env python

from mesonbuild.ast.visitor import AstVisitor
from mesonbuild.mparser import Parser, FunctionNode, StringNode
from tempfile import TemporaryDirectory
from os import system, chdir
from shutil import copytree
from pathlib import Path
from sys import stdin

FORBIDDEN_FUNCTIONS = ["run_command",
                       "files", "find_program", "configure_file"]
DANGEROUS_STRINGS = ["/bin", "sh", "bash", "zsh", "ksh", "cat", "tac"]


class MyVisitor(AstVisitor):
    def visit_FunctionNode(self, node: FunctionNode) -> None:
        if node.func_name in FORBIDDEN_FUNCTIONS:
            print(f"{node.func_name} is a FORBIDDEN FUNCTION\nExiting...")
            exit()

    def visit_StringNode(self, node: StringNode) -> None:
        if any(map(lambda danger: danger in node.value, DANGEROUS_STRINGS)):
            print(f"'{node.value}' contains a DANGEROUS STRINGS\nExiting...")
            exit()


def main():
    with TemporaryDirectory() as dir:
        chdir(dir)
        copytree("/home/user/", dir, dirs_exist_ok=True)

        print("We will setup jail according to your instructions.")
        print("Please provide build instructions.")
        # user_input = "".join(line for line in stdin)

        user_input = ""
        while (line := input()) != "EOF":
            user_input += line + "\n"

        p = Parser(user_input, '').parse()
        p.accept(MyVisitor())

        Path("meson.build").write_text(user_input)
        system(f"meson setup builddir")


main()
