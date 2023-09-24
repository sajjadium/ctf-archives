#!/usr/local/bin/python
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Flag is in a file called "flag" in cwd.
#
# Quote from Dockerfile:
#   FROM ubuntu:22.04
#   RUN apt-get update && apt-get install -y python3
#

if __name__ != "__main__":
    1/0  # Not a module

import ast
import sys
import os


def verify_secure(m):
    for x in ast.walk(m):
        match type(x):
            case (ast.Lambda | ast.alias | ast.Assign | ast.Add | ast.Subscript | ast.Dict | ast.Store | ast.arg | ast.Pow | ast.Expr | ast.Div | ast.BinOp | ast.Sub | ast.Name | ast.Mult | ast.Module | ast.Load | ast.Constant | ast.Import | ast.ClassDef | ast.arguments | ast.UnaryOp | ast.USub):
                continue
            case _:
                print(f"ERROR: Banned statement {x}")
                return False
    return True


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

print("-- Please enter code (last line must contain only --END, will be split by --CHUNK)")
source_code = ""
while True:
    line = input() + "\n"
    if line.startswith("--END"):
        break
    source_code += line

if '@' in source_code or '.' in source_code or '(' in source_code or ')' in source_code or '#' in source_code:
    print("ERROR: @.()# are banned")
    exit(1)


chunks = source_code.split("--CHUNK\n")
for chunk in chunks:
    tree = compile(source_code, "input.py", 'exec', flags=ast.PyCF_ONLY_AST)
    if not verify_secure(tree):
        exit(1)

for chunk in chunks:  # Safe to execute!
    print("-- Executing safe code:")
    print(chunk)
    exec(chunk)