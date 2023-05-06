cmake_minimum_required(VERSION 3.8)
project(minilang)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

add_executable(minilang
        src/main.cpp
        src/lexer/lexer.cpp
        src/lexer/lexer.h
        src/lexer/token.cpp
        src/lexer/token.h
        src/parser/parser.cpp
        src/parser/parser.h
        src/parser/ast.cpp
        src/parser/ast.h
        src/visitor/visitor.h
        src/visitor/xml_visitor.cpp
        src/visitor/xml_visitor.h
        src/visitor/semantic_analysis.cpp
        src/visitor/semantic_analysis.h
        src/visitor/interpreter.cpp
        src/visitor/interpreter.h
        src/optimizer/optimizer.cpp
        src/optimizer/optimizer.h
        src/table/table.h)
