/**
 * @file token.cpp
 * Implements the functions in token.h
  * @author Luke Collins
 * @date 19/3/2018
 */
#include "token.h"

using namespace lexer;

Token::Token() = default;

Token::Token(int final_state, std::string value, unsigned int line_number) :
    type(determine_token_type(final_state, value)),
    value(value),
    line_number(line_number)
{}

TOKEN Token::determine_token_type(int final_state, std::string &value) {
    switch(final_state) {
        case 1:
            return TOK_INT;

        case 3:
            return TOK_REAL;

        case 4:
            return TOK_ADDITIVE_OP;

        case 5:
        case 11:
            return TOK_MULTIPLICATIVE_OP;

        case 7:
            return TOK_RELATIONAL_OP;

        case 8:
            return TOK_EQUALS;

        case 9:
            return TOK_RELATIONAL_OP;

        case 10:
            if(value == "var")
                return TOK_VAR;
            if(value == "set")
                return TOK_SET;
            if(value == "def")
                return TOK_DEF;
            if(value == "return")
                return TOK_RETURN;
            if(value == "if")
                return TOK_IF;
            if(value == "else")
                return TOK_ELSE;
            if(value == "while")
                return TOK_WHILE;
            if(value == "print")
                return TOK_PRINT;
            if(value == "int")
                return TOK_INT_TYPE;
            if(value == "real")
                return TOK_REAL_TYPE;
            if(value == "bool")
                return TOK_BOOL_TYPE;
            if(value == "string")
                return TOK_STRING_TYPE;
            if(value == "true" || value == "false")
                return TOK_BOOL;
            if(value == "and")
                return TOK_MULTIPLICATIVE_OP;
            if(value == "or")
                return TOK_ADDITIVE_OP;
            if(value == "not")
                return TOK_NOT;
            else return TOK_IDENTIFIER;

        case 14:
        case 16:
            return TOK_COMMENT;

        case 20:
            return TOK_STRING;

        case 21:
            if(value == "{")
                return TOK_LEFT_CURLY;
            if(value == "}")
                return TOK_RIGHT_CURLY;
            if(value == "(")
                return TOK_LEFT_BRACKET;
            if(value == ")")
                return TOK_RIGHT_BRACKET;
            if(value == ",")
                return TOK_COMMA;
            if(value == ";")
                return TOK_SEMICOLON;
            if(value == ":")
                return TOK_COLON;

        case 22:
            return TOK_EOF;

        default:
            return TOK_ERROR;
    }
}